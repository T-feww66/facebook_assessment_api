from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401
from typing import Optional

from app.models.danh_gia import DanhGia
from app.security.security import get_api_key

from danh_gia_thuong_hieu.utils.danh_gia_tot_xau import DanhGiaTotXau
from chatbot.services.evaluate_total import EvaluateTotal
from chatbot.services.evaluate_compare import EvaluateCompare

#database
from database.db.brands_repository import BrandsRepository

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
        result = BrandsRepository().get_data_llm_by_brand_name(brand_name=brand_name)

        if not result:
            raise HTTPException(status_code=404, detail="Không tìm thấy thương hiệu trong CSDL. Chúng tôi sẻ cập nhật sau")

        try:
            data_llm = json.loads(result["data_llm"])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi đọc JSON từ data_llm: {str(e)}")
        
        # 2. Tạo prompt
        prompt = f"{brand_name}: {data_llm}"

        # 3. Gọi workflow AI (EvaluateTotal)
        chat = EvaluateTotal().get_workflow().compile().invoke(
            input={"question": prompt}
        )
        response = chat["generation"]
        return DanhGia(id="chatbot-response-evaluate", data=response)

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")


# cấu hình router so sánh hai thương hiệu
@router.post("/so_sanh_thuong_hieu", response_model=DanhGia)
async def compare_brands(
    api_key: str = get_api_key,
    brand1: str = Form(""),
    brand2: str = Form(""),
):
    try:
        brand1 = brand1.strip()
        brand2 = brand2.strip()

        # 1. Lấy dữ liệu từ DB cho cả hai thương hiệu
        result1 = BrandsRepository().get_data_llm_by_brand_name(brand_name=brand1)
        result2 = BrandsRepository().get_data_llm_by_brand_name(brand_name=brand2)

        if not result1 or not result2:
            raise HTTPException(status_code=404, detail="Không tìm thấy dữ liệu một trong hai thương hiệu.")

        try:
            data_llm_1 = json.loads(result1["data_llm"])
            data_llm_2 = json.loads(result2["data_llm"])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi đọc JSON từ data_llm: {str(e)}")

        # 2. Tạo prompt so sánh
        prompt = (
            f"So sánh hai thương hiệu sau đây:\n\n"
            f"Thương hiệu 1: Tên:{brand1}: \n Dữ liệu phân tích:{data_llm_1}\n\n"
            f"Thương hiệu 1: Tên:{brand2}: \n Dữ liệu phân tích:{data_llm_2}\n\n"
        )

        # 3. Gọi workflow AI (có thể tái dùng EvaluateTotal nếu không cần thay đổi)
        chat = EvaluateCompare().get_workflow().compile().invoke(
            input={"question": prompt}
        )
        response = chat["generation"]
        return DanhGia(id="chatbot-response-compare", data=response)

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")