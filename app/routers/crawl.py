from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401

# import file chat agent
from app.models.crawl import Crawl
from app.security.security import get_api_key

#crawl data
from crawl_data.services.crawl_comments_groups import CrawlCommentGroup
from crawl_data.services.crawl_comments_fanpage import CrawlCommentFanpage
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.responses import JSONResponse

# đánh giá
from danh_gia_thuong_hieu.utils.danh_gia_tot_xau import DanhGiaTotXau
from database.db.brands_repository import BrandsRepository
from database.db.user_send_request_repository import UserSendRequestRepository
from app.models.danh_gia import DanhGia

#send mail 
from crawl_data.utils.send_mail import send_email_confirm_review

from urllib.parse import unquote

import os
import platform



# Tạo router cho người dùng
router = APIRouter(prefix="/crawl", tags=["crawl"])

# Đường dẫn thư mục chứa file CSV
CSV_DIR = "crawl_data/data/comments"

# Lấy hệ điều hành hiện tại
system = platform.system()
if system == "Windows":
    driver_path = "crawl_data/chrome_driver/chromedriver.exe"
else:
    driver_path = "crawl_data/chrome_driver/chromedriver"

#router cho cào dữ liệu
@router.post("/crawl_comment_of_groups", response_model=Crawl)
async def crawl_comment_groups(
    api_key: str = get_api_key,  # Khóa API để xác thực
    name_group: str = Form(""),
    word_search: str = Form(""),
    quantity_group: int = Form(""),
    quantity_post_of_group: int = Form(""),
):
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"         
        crawler = CrawlCommentGroup(word_search=word_search, name_group=name_group,  quantity_group=quantity_group,
                              chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, quantity_post_of_group=quantity_post_of_group)
        file_save = crawler.crawl()
        crawler.close()

        #đánh giá thương hiệu
        if os.path.exists(file_save):
            danh_gia = DanhGiaTotXau()
            danh_gia.run_review(comment_file=file_save)
            
            return Crawl(id="anhlong", data = {"message": "Đánh giá thành công và cập nhật vào cơ sở dữ liệu"})

        raise HTTPException(status_code=404, detail="File not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")


@router.post("/crawl_comment_of_fanpages", response_model=Crawl)
async def crawl_comment_fanpages(
    api_key: str = get_api_key,  # Khóa API để xác thực
    word_search: str = Form(""),
    quantity_post_of_fanpage: int = Form(...),
):
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"           
        crawler = CrawlCommentFanpage(word_search=word_search,
                              chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, quantity_post_of_fanpage=quantity_post_of_fanpage)
        
        file_save = crawler.crawl()
        crawler.close()

        if os.path.exists(file_save):
            danh_gia = DanhGiaTotXau()
            danh_gia.run_review(comment_file=file_save)
            
            repo = UserSendRequestRepository()
            result = repo.get_user_send_request_by_brand_name(brand_name=word_search)

            if result:
                repo.update_status_by_id(id = result["id"], status=1)
                send_email_confirm_review(
                    to_email=result["email"],
                    brand_name=word_search,
                    dashboard_link="http://127.0.0.1:8000/user/tim-kiem"
                )
                return Crawl(id="xcanahnmlai", data={"message": "Đã gửi mail xác nhận cho người dùng"})
             
            return Crawl(id="anhlong", data = {"message": "Đánh giá thành công và cập nhật vào cơ sở dữ liệu"})

        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

  
#router download file
@router.get("/download/{filename}")
def download_file(filename: str):
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
    try:
        files = [f for f in os.listdir(CSV_DIR) if f.endswith(".csv")]
        return {"csv_files": files}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found")


# xoa csv
@router.delete("/delete-csv-file/{filename}")
def delete_csv_file(filename: str):

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
