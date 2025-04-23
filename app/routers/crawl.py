from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401

# import file chat agent
from app.models.crawl import Crawl
from app.security.security import get_api_key

# Driver 
from crawl_data.utils.driver import Driver

#crawl data
from crawl_data.scrapers.crawl_groups import CrawlGroup
from crawl_data.scrapers.crawl_fanpage import CrawlFanPage


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

from crawl_data.utils.find_filename_by_keyword import find_files_by_keyword
from urllib.parse import unquote

import asyncio
import pandas as pd
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
    api_key: str = get_api_key,
    group_urls: list = Form(...),
    word_search: str = Form(""),
):
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"         
        crawler = CrawlCommentGroup(word_search=word_search, 
                            chrome_driver_path=chrome_driver_path, 
                            list_url_group = group_urls,
                            cookies_file=cookies_file)
        file_save = crawler.crawl()
        crawler.close()

        #đánh giá thương hiệu
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
                    dashboard_link=f"http://127.0.0.1:8000/user/tim-kiem/{word_search}"
                )
                return Crawl(id="xcanahnmlai", data={"message": "Đã gửi mail xác nhận cho người dùng"})
            return Crawl(id="anhlong", data = {"message": "Đánh giá thành công và cập nhật vào cơ sở dữ liệu"})

        raise HTTPException(status_code=404, detail="File not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")


@router.post("/crawl_comment_of_fanpages", response_model=Crawl)
async def crawl_comment_fanpages(
    api_key: str = get_api_key,  # Khóa API để xác thực
    word_search: str = Form(""),
    fanpage_urls: list = Form(...),
):
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"           
        crawler = CrawlCommentFanpage(word_search=word_search,
                              chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, fanpage_urls=fanpage_urls)
        
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
                    dashboard_link=f"http://127.0.0.1:8000/user/tim-kiem/{word_search}"
                )
                return Crawl(id="xcanahnmlai", data={"message": "Đã gửi mail xác nhận cho người dùng"})
             
            return Crawl(id="anhlong", data = {"message": "Đánh giá thành công và cập nhật vào cơ sở dữ liệu"})

        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")


@router.post("/get_url_groups")
async def get_url_groups(
    api_key: str = get_api_key,  # Khóa API để xác thực
    quantity_group: int = Form(...),
    word_search_group: str = Form(""),
):
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"  

        # Nơi lưu file dữ liệu url khi crawl xong 
        folder_group_save_file = "crawl_data/data/group/"
        save_group_file = f"crawl_data/data/group/{word_search_group}.csv"

        matching_files_group = find_files_by_keyword(folder_group_save_file, word_search_group)
        # check file group đã lưu chưa
        if matching_files_group:
            group = pd.read_csv(matching_files_group[0])
            data = group.to_dict(orient="records")
            return JSONResponse(content=data)
             
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
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
    
@router.post("/get_url_fanpages")
async def get_url_fanpages(
    api_key: str = get_api_key,  # Khóa API để xác thực
    quantity_fanpage: int = Form(...),
    word_search_pages: str = Form(""),
):
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"   
        folder_fanpages_save_file = "crawl_data/data/fanpages/"
        save_fanpages_file = f"crawl_data/data/fanpages/{word_search_pages}.csv"

        matching_files_fanpage = find_files_by_keyword(folder_fanpages_save_file, word_search_pages)
         # check file group đã lưu chưa
        if matching_files_fanpage:
            fanpages = pd.read_csv(matching_files_fanpage[0])
            data = fanpages.to_dict(orient="records")
            return JSONResponse(content=data)
        
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
