from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401

from app.models.danh_gia import DanhGia
from app.security.security import get_api_key

from danh_gia_thuong_hieu.utils.danh_gia_tot_xau import DanhGiaTotXau

import os

# Tạo router cho người dùng
router = APIRouter(prefix="/danh_gia_thuong_hieu", tags=["danh_gia_thuong_hieu"])

@router.post("/danh_gia/", response_model=DanhGia)
async def comments(
        api_key: str = get_api_key,  # Khóa API để xác thực
        comments_file: str = Form(""),
):
    file_path = os.path.join("crawl_data", "data", "comments", comments_file)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        danh_gia = DanhGiaTotXau()
        danh_gia.run_review(comment_file=file_path)
        return {"message": "Đánh giá thành công"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")