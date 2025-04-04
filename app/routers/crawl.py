from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401

from app.models.crawl import Crawl

# import file chat agent
from app.security.security import get_api_key
from app.config import settings

#crawl data
from crawl_data.services.crawl_comments_groups import CrawlCommentGroup
from crawl_data.services.crawl_comments_fanpage import CrawlCommentFanpage
# Tạo router cho người dùng
router = APIRouter(prefix="/crawl", tags=["crawl"])


# @router.post("/base-url/", response_model=Base)
# async def base_url(
#     api_key: str = get_api_key,  # Khóa API để xác thực
#     base_data: str = Form(""),
# ):

#     return Base(id="EKcG&@(t|x_8xr/`ObZb|uQ+^'[i_L", data=base_data)
#router cho cào dữ liệu

@router.post("/crawl_comment_of_groups", response_model=Crawl)
async def crawl_comment_groups(
    api_key: str = get_api_key,  # Khóa API để xác thực
    word_search: str = Form(""),
    quantity_group: int = Form(""),
    quantity_post_of_group: int = Form(""),
):
    try:
        chrome_driver_path = "crawl_data\chrome_driver\chromedriver.exe"
        cookies_file = "crawl_data\data\cookies\my_cookies.pkl"
               
        crawler = CrawlCommentGroup(word_search=word_search, quantity_group=quantity_group, chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, quantity_post_of_group=quantity_post_of_group)
        file_save = crawler.crawl()
        crawler.close()
        return Crawl(id="bot-crawl-respone", data=f"Dữ liệu lưu trữ trong {file_save}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")


@router.post("/crawl_comment_of_fanpages", response_model=Crawl)
async def crawl_comment_fanpages(
    api_key: str = get_api_key,  # Khóa API để xác thực
    word_search: str = Form(""),
    quantity_fanpage: int = Form(""),
    quantity_post_of_fanpge: int = Form(""),
):
    try:
        chrome_driver_path = "crawl_data\chrome_driver\chromedriver.exe"
        cookies_file = "crawl_data\data\cookies\my_cookies.pkl"           
        crawler = CrawlCommentFanpage(word_search=word_search, quantity_fanpage=quantity_fanpage, chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, quantity_post_of_fanpage=quantity_post_of_fanpge)
        file_save = crawler.crawl()
        crawler.close()
        return Crawl(id="bot-crawl-respone", data=f"Dữ liệu lưu trữ trong {file_save}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")