from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form, BackgroundTasks # noqa: E402, F401

# import file chat agent
from app.models.crawl import Crawl
from app.security.security import get_api_key

# Driver 
from crawl_data.utils.driver import Driver

#crawl data
from crawl_data.scrapers.crawl_groups import CrawlGroup
from crawl_data.scrapers.crawl_fanpage import CrawlFanPage


from crawl_data.services.crawl_comments_groups import CrawlCommentGroup
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.responses import JSONResponse

# đánh giá
from danh_gia_thuong_hieu.utils.danh_gia_tot_xau import DanhGiaTotXau
from database.db.crawl_url_repository import CrawlUrlRepository
from database.db.user_send_request_repository import UserSendRequestRepository
from app.models.danh_gia import DanhGia

#send mail 
from crawl_data.utils.send_mail import send_email_confirm_review

from crawl_data.utils.find_filename_by_keyword import find_files_by_keyword
from urllib.parse import unquote

import asyncio
import pandas as pd
import os
import platform
from datetime import datetime

import queue
import uuid


crawl_queue = queue.Queue()

# Tạo router cho người dùng
router = APIRouter(prefix="/crawl", tags=["crawl"])

# Đường dẫn thư mục chứa file CSV
CSV_DIR = "crawl_data/data/comments"
COOKIES_DIR = "crawl_data/data/cookies"

# Lấy hệ điều hành hiện tại
system = platform.system()
if system == "Windows":
    driver_path = "crawl_data/chrome_driver/chromedriver.exe"
else:
    driver_path = "crawl_data/chrome_driver/chromedriver"

#router cho cào dữ liệu
@router.post("/crawl_comment_of_groups", response_model=Crawl)
async def crawl_comment_groups(
    api_key: str = get_api_key,
    crawl_url_link: list = Form(...),
    crawl_url_name: list = Form(...),
    brand_name: str = Form(""),
    word_search: str = Form(""),
    user_id: int = Form(...),
):
    """
    API để thu thập và đánh giá dữ liệu comments từ các group Facebook dựa trên `word_search`.

    API này thực hiện 2 chức năng chính:
    1. Thu thập dữ liệu comment từ danh sách các group Facebook được cung cấp.
    2. Đánh giá từng comment đã thu thập được để xác định là tích cực hay tiêu cực, sau đó phân loại vào các nhóm tương ứng.

    Tham số:
    - `api_key` (str): Khóa API để xác thực.
    - `crawl_url_link` (list): Danh sách URL các group Facebook cần thu thập dữ liệu.
    - `crawl_url_name` (list): Danh sách tên các nhóm Facebook tương ứng với `crawl_url_link`.
    - `brand_name` (str): Tên thương hiệu để lọc dữ liệu và kiểm tra yêu cầu đánh giá (mặc định là chuỗi rỗng).
    - `word_search` (str): Từ khóa tìm kiếm (ví dụ: tên thương hiệu hoặc từ khóa liên quan).
    - `user_id` (int): ID người dùng để lưu trữ yêu cầu.

    Trả về:
    - `id` (int): Định danh phản hồi.
    - `data` (str): Thông điệp phản hồi, có thể là thông báo đã cập nhật đánh giá vào cơ sở dữ liệu.

    Lỗi có thể gặp:
    - `404`: Không tìm thấy dữ liệu hoặc tài nguyên liên quan đến từ khóa.
    - `500`: Lỗi hệ thống trong quá trình xử lý, ví dụ như lỗi từ chatbot hoặc lỗi khi lưu dữ liệu vào cơ sở dữ liệu.
    """

    word_search = word_search.lower().strip()
    brand_name = brand_name.lower().strip()

    crawl_url_group_repo = CrawlUrlRepository()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request_id = str(uuid.uuid4())
    number = len(crawl_url_link)

    # 1. Ghi vào bảng user_send_request với status = 0
    user_request_repo = UserSendRequestRepository()
    user_request_repo.insert_request(
        id = request_id,
        user_id = user_id,
        brand_name = brand_name,
        word_search = word_search,
        status = 0
    )

    # 2. Đưa vào hàng đợi để xử lý nền
    crawl_queue.put({
        "request_id": request_id,
        "user_id": user_id,
        "brand_name": brand_name,
        "word_search": word_search,
        "crawl_url_link": crawl_url_link,
        "crawl_url_name": crawl_url_name,
        "type": 0
    })

    crawl_url_group_repo.insert_or_update_many(crawl_url_link, crawl_url_name, [brand_name]*number, [now]*number, [now]*number)
    return Crawl(id=request_id, data={"message": "Đã nhận yêu cầu đánh giá, chúng tôi sẽ gửi kết quả sau."})


@router.post("/crawl_comment_of_fanpages", response_model=Crawl)
async def crawl_comment_fanpages(
    background_tasks: BackgroundTasks,
    api_key: str = get_api_key,  # Khóa API để xác thực
    word_search: str = Form(""),
    brand_name: str = Form(""),
    crawl_url_link: list = Form(...),
    crawl_url_name: list = Form(...),
    user_id: int = Form(...),
):
    """
    API để thu thập và đánh giá dữ liệu comments từ các fanpage Facebook dựa trên danh sách URL fanpage được cung cấp.

    API này thực hiện 2 chức năng chính:
    1. Thu thập dữ liệu comment từ danh sách các fanpage Facebook được cung cấp.
    2. Đánh giá từng comment đã thu thập được để xác định là tích cực hay tiêu cực, sau đó phân loại vào các nhóm tương ứng.

    Tham số:
    - `api_key` (str): Khóa API để xác thực.
    - `word_search` (str): Tên thương hiệu cần đánh giá.
    - `brand_name` (str): Tên thương hiệu để lọc và kiểm tra dữ liệu thu thập được.
    - `crawl_url_link` (list): Danh sách URL các fanpage Facebook cần thu thập dữ liệu.
    - `crawl_url_name` (list): Danh sách tên các fanpage tương ứng với URL trong `crawl_url_link`.
    - `user_id` (int): ID người dùng để lưu trữ yêu cầu.

    Trả về:
    - `id` (int): Định danh phản hồi.
    - `data` (str): Thông điệp phản hồi, có thể là thông báo đã cập nhật đánh giá vào cơ sở dữ liệu.

    Lỗi có thể gặp:
    - `404`: Không tìm thấy dữ liệu hoặc tài nguyên liên quan đến từ khóa.
    - `500`: Lỗi hệ thống trong quá trình xử lý, ví dụ như lỗi từ chatbot hoặc lỗi khi lưu dữ liệu vào cơ sở dữ liệu.
    """
    word_search = word_search.lower().strip()
    brand_name = brand_name.lower().strip()

    crawl_url_page_repo = CrawlUrlRepository()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request_id = str(uuid.uuid4())
    number = len(crawl_url_link)

    # 1. Ghi vào bảng user_send_request với status = 0
    user_request_repo = UserSendRequestRepository()
    user_request_repo.insert_request(
        id = request_id,
        user_id = user_id,
        brand_name = brand_name,
        word_search = word_search,
        status = 0
    )

    # 2. Đưa vào hàng đợi để xử lý nền
    crawl_queue.put({
        "request_id": request_id,
        "user_id": user_id,
        "brand_name": brand_name,
        "word_search": word_search,
        "crawl_url_link": crawl_url_link,
        "crawl_url_name": crawl_url_name,
        "type": 1
    })

    crawl_url_page_repo.insert_or_update_many(crawl_url_link, crawl_url_name, [brand_name]*number, [now]*number, [now]*number)
    return Crawl(id=request_id, data={"message": "Đã nhận yêu cầu đánh giá, chúng tôi sẽ gửi kết quả sau."})


@router.post("/get_url_groups")
async def get_url_groups(
    api_key: str = get_api_key,  # Khóa API để xác thực
    quantity_group: int = Form(...),
    word_search_group: str = Form(""),
):
    """
        API để crawl tên và url của các group Facebook liên quan đến thương hiệu.

        Tham số:
        - `api_key`: Khóa API để xác thực.
        - `quantity_group`: Số lượng group cần truy vấn.
        - `word_search_group`: Từ khóa tìm kiếm (tên thương hiệu).

        Trả về:
        - Dữ liệu JSON chứa danh sách group và url tương ứng.

        Lỗi có thể gặp:
        - `404`: Không tìm thấy các group về thương hiệu này.
        - `500`: Lỗi hệ thống khi xử lý yêu cầu (ví dụ: lỗi nội bộ từ crawl hoặc xử lý dữ liệu).

        API này thực hiện tìm kiếm các group Facebook theo từ khóa chỉ định, giới hạn số lượng theo `quantity_group`. Kết quả trả về là dữ liệu về tên và url của các group.
    """
    word_search_group = word_search_group.lower().strip()
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"  

        # Nơi lưu file dữ liệu url khi crawl xong 
        folder_group_save_file = "crawl_data/data/group/"
        save_group_file = f"crawl_data/data/group/{word_search_group}.csv"

        # check = find_files_by_keyword(folder_path=folder_group_save_file, keyword=word_search_group)
        # if check:
        #     group = pd.read_csv(check[0])
        #     if len(group) >= quantity_group:
        #         data = group[:quantity_group].to_dict(orient="records")
        #         return JSONResponse(content=data)
        
        driver = Driver(chrome_driver_path=chrome_driver_path,
                headless=True,
        ).get_driver()
        group = CrawlGroup(driver=driver, cookies_file=cookies_file).crawl_group_url(quantity_group = quantity_group, word_search=word_search_group, output_file=save_group_file)
        driver.quit()

        if not group.empty:
            data = group.to_dict(orient="records")   
            return JSONResponse(content=data)
        
        raise HTTPException(status_code=404, detail="Không tìm thấy các group về thương hiệu này")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crawl error: {str(e)}")
    
@router.post("/get_url_fanpages")
async def get_url_fanpages(
    api_key: str = get_api_key,  # Khóa API để xác thực
    quantity_fanpage: int = Form(...),
    word_search_pages: str = Form(""),
):
    """
        API để crawl tên và url của các page Facebook liên quan đến thương hiệu.

        Tham số:
        - `api_key`: Khóa API để xác thực.
        - `quantity_fanpage`: Số lượng page cần truy vấn.
        - `word_search_pages`: Từ khóa tìm kiếm (tên thương hiệu).

        Trả về:
        - Dữ liệu JSON chứa danh sách page và url tương ứng.

        Lỗi có thể gặp:
        - `404`: Không tìm thấy các page về thương hiệu này.
        - `500`: Lỗi hệ thống khi xử lý yêu cầu (ví dụ: lỗi nội bộ từ crawl hoặc xử lý dữ liệu).

        API này thực hiện tìm kiếm các group Facebook theo từ khóa chỉ định, giới hạn số lượng theo `quantity_fanpage`. Kết quả trả về là dữ liệu về tên và url của các page.
    """
    word_search_pages = word_search_pages.lower().strip()
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"
        folder_group_save_file = "crawl_data/data/fanpages/"
        save_fanpages_file = f"crawl_data/data/fanpages/{word_search_pages}.csv"

        # check = find_files_by_keyword(folder_path=folder_group_save_file, keyword=word_search_pages)
        # if check:
        #     pages = pd.read_csv(check[0])
        #     if len(pages) >= quantity_fanpage:
        #         data = pages[:quantity_fanpage].to_dict(orient="records")
        #         return JSONResponse(content=data)
        
        driver = Driver(chrome_driver_path=chrome_driver_path,
                headless=True,
        ).get_driver()
        fanpages = CrawlFanPage(driver=driver, cookies_file=cookies_file).crawl_fanpage_url(quantity=quantity_fanpage, word_search=word_search_pages, output_file=save_fanpages_file)
        driver.quit()

        if not fanpages.empty:
            data = fanpages.to_dict(orient="records")   
            return JSONResponse(content=data)
          
        raise HTTPException(status_code=404, detail="Không tìm thấy các fanpages về thương hiệu này")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crawl error: {str(e)}")
    

#router download file
@router.get("/download/{filename}")
def download_file(filename: str):
    """
        API để tải xuống tệp dữ liệu đã thu thập từ hệ thống.

        Tham số:
        - `filename`: Tên tệp cần tải xuống (bao gồm cả đuôi mở rộng, ví dụ: "comments.csv").

        Trả về:
        - Tệp tương ứng với `filename` dưới dạng file đính kèm (attachment).

        Lỗi có thể gặp:
        - `404`: Không tìm thấy tệp yêu cầu.

        API này cho phép người dùng tải xuống tệp dữ liệu (ví dụ: các bình luận đã crawl) từ thư mục lưu trữ nội bộ của hệ thống.
    """
    file_path = os.path.join("crawl_data", "data", "comments", filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    raise HTTPException(status_code=404, detail="File not found")

# List csv
@router.get("/list-csv-files")
def list_csv_files():
    """
        API để liệt kê tất cả các tệp CSV có trong thư mục.

        Tham số:
        - Không có tham số đầu vào.

        Trả về:
        - `csv_files`: Danh sách tên các tệp có đuôi `.csv` trong thư mục.

        Lỗi có thể gặp:
        - `404`: Không tìm thấy thư mục chứa các tệp CSV.

        API này sẽ trả về danh sách các tệp `.csv` có trong thư mục được chỉ định, phục vụ cho việc quản lý và thao tác với các tệp dữ liệu.
    """

    try:
        files = [f for f in os.listdir(CSV_DIR) if f.endswith(".csv")]
        return {"csv_files": files}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found")


# xoa csv
@router.delete("/delete-csv-file/{filename}")
def delete_csv_file(filename: str):
    """
        API để xoá tệp CSV khỏi thư mục.

        Tham số:
        - `filename`: Tên tệp CSV cần xoá (bao gồm cả đuôi mở rộng, ví dụ: "data.csv").

        Trả về:
        - `success`: Trạng thái xoá tệp (True nếu xoá thành công).
        - `message`: Thông báo về kết quả xoá tệp.

        Lỗi có thể gặp:
        - `400`: Tệp không phải là tệp CSV.
        - `404`: Không tìm thấy tệp yêu cầu.
        - `500`: Lỗi hệ thống khi xoá tệp.

        API này cho phép người dùng xoá một tệp CSV cụ thể khỏi thư mục lưu trữ.
    """
    filename = unquote(filename)
    file_path = os.path.join(CSV_DIR, filename)
    
    if not filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        os.remove(file_path)
        return JSONResponse(content={"success": True, "message": f"{filename} deleted successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete-all-cookies-files")
def delete_all_files():
    """
        API để xoá tất cả các tệp trong thư mục cookies.

        Tham số:
        - Không có tham số đầu vào.

        Trả về:
        - `success`: Trạng thái xoá thành công (True nếu đã xoá ít nhất một tệp).
        - `deleted_files`: Danh sách các tệp đã bị xoá.
        - `message`: Thông báo về số lượng tệp đã xoá.

        Lỗi có thể gặp:
        - `500`: Lỗi hệ thống khi xoá các tệp (ví dụ: không có quyền xoá tệp, lỗi truy xuất thư mục).

        API này thực hiện xoá tất cả các tệp trong thư mục cookies, bỏ qua các thư mục con. Nếu có tệp bị xoá, danh sách các tệp đã xoá sẽ được trả về.
    """

    try:
        deleted_files = []

        for filename in os.listdir(COOKIES_DIR):
            file_path = os.path.join(COOKIES_DIR, filename)
            if os.path.isfile(file_path):  # Chỉ xoá file, không xoá folder
                os.remove(file_path)
                deleted_files.append(filename)

        return JSONResponse(content={
            "success": True,
            "deleted_files": deleted_files,
            "message": f"Deleted {len(deleted_files)} file(s) from cookies directory."
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
