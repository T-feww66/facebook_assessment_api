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

        if os.path.exists(file_save):
            filename = os.path.basename(file_save)
            return Crawl(id="bot-crawl-respone", data={
                    "message": f"Dữ liệu đã được lưu vào {file_save}",
                    "download_url": f"/download/{filename}"
                })
        raise HTTPException(status_code=404, detail="File not found") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")


@router.post("/crawl_comment_of_fanpages", response_model=Crawl)
async def crawl_comment_fanpages(
    api_key: str = get_api_key,  # Khóa API để xác thực
    word_search: str = Form(""),
    quantity_fanpage: int = Form(""),
    quantity_post_of_fanpage: int = Form(""),
):
    try:
        chrome_driver_path = driver_path
        cookies_file = "crawl_data/data/cookies/my_cookies.pkl"           
        crawler = CrawlCommentFanpage(word_search=word_search, quantity_fanpage=quantity_fanpage,
                              chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, quantity_post_of_fanpage=quantity_post_of_fanpage)
        
        file_save = crawler.crawl()
        crawler.close()

        if os.path.exists(file_save):
            filename = os.path.basename(file_save)
            return Crawl(id="bot-crawl-respone", data={
                    "message": f"Dữ liệu đã được lưu vào {file_save}",
                    "download_url": f"/download/{filename}"
                })

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
