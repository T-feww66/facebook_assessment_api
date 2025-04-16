from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401
from typing import Optional

from app.models.danh_gia import DanhGia
from app.security.security import get_api_key

from danh_gia_thuong_hieu.utils.danh_gia_tot_xau import DanhGiaTotXau

#database
from database.db.brands_repository import BrandsRepository
from database.db.comment_crawl_repository import CommentRepository
import os
import json

# Tạo router cho người dùng
router = APIRouter(prefix="/danh_gia_thuong_hieu", tags=["danh_gia_thuong_hieu"])

@router.post("/danh_gia", response_model=DanhGia)
async def comments(
        api_key: str = get_api_key,  # Khóa API để xác thực
        comments_file: str = Form(""),
        limit: Optional[int] = Form(None),
):
    file_path = os.path.join("crawl_data", "data", "comments", comments_file)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        danh_gia = DanhGiaTotXau()
        danh_gia.run_review(comment_file=file_path, limit=limit)
        return DanhGia(id="anhlong", data = {"message": "Đánh giá thành công và cập nhật vào cơ sở dữ liệu"}) 
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/thuong_hieu", response_model=DanhGia) 
async def evaluate_total( 
    api_key: str = get_api_key, 
    brand: str = Form(""),
):
    try: 
        brand_name = brand.strip()
        # 1. Kết nối và truy vấn MySQL
        result = CommentRepository().get_crawl_comment_by_name(brand_name=brand_name)
        if not result:
            raise HTTPException(status_code=404, detail="Không tìm thấy thương hiệu trong CSDL. Chúng tôi sẻ cập nhật sau")

        try:
            return DanhGia(id="chatbot-response-evaluate", data=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi đọc JSON từ data: {str(e)}")
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")