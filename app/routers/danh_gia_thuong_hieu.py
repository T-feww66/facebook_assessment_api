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
import ast

# Tạo router cho người dùng
router = APIRouter(prefix="/danh_gia_thuong_hieu", tags=["danh_gia_thuong_hieu"])

@router.post("/thuong_hieu", response_model=DanhGia) 
async def evaluate_total( 
    api_key: str = get_api_key, 
    brand: str = Form(""),
):
    try: 
        brand_name = brand.strip()
        # 1. Kết nối và truy vấn MySQL
        result = BrandsRepository().get_data_brands_crawl_comments(brand_name=brand_name)
        if not result:
            raise HTTPException(status_code=404, detail="Không tìm thấy thương hiệu trong CSDL.")

        try:
            for item in result:
                item["brand_data_llm"] = json.loads(item["brand_data_llm"])
                item["comment_data_llm"] = json.loads(item["comment_data_llm"])

                item["brand_data_llm"]["danh_sach_tu_tot"] = ast.literal_eval(item["brand_data_llm"]["danh_sach_tu_tot"].replace("\\\"", "\"").replace("\\'", "'"))
                item["brand_data_llm"]["danh_sach_tu_xau"] = ast.literal_eval(item["brand_data_llm"]["danh_sach_tu_xau"].replace("\\\"", "\"").replace("\\'", "'"))
                item["comment_data_llm"]["danh_sach_tu_tot"] = ast.literal_eval(item["comment_data_llm"]["danh_sach_tu_tot"].replace("\\\"", "\"").replace("\\'", "'"))
                item["comment_data_llm"]["danh_sach_tu_xau"] = ast.literal_eval(item["comment_data_llm"]["danh_sach_tu_xau"].replace("\\\"", "\"").replace("\\'", "'"))
            return DanhGia(id="chatbot-response-evaluate", data=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi đọc JSON từ data: {str(e)}")
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
    
@router.post("/so_sanh_thuong_hieu", response_model=DanhGia)
async def compare_brands(
    api_key: str = get_api_key,
    brand_1: str = Form(""),
    brand_2: str = Form(""),
):
    try:
        brand_name_1 = brand_1.strip()
        brand_name_2 = brand_2.strip()

        if brand_name_1 == brand_name_2:
            raise HTTPException(status_code=404, detail="Thương hiệu bị trùng vui lòng nhập thương hiệu khác nhau để so sánh")

        # Truy vấn dữ liệu cho từng thương hiệu
        result_1 = BrandsRepository().get_data_brands_crawl_comments(brand_name=brand_name_1)
        result_2 = BrandsRepository().get_data_brands_crawl_comments(brand_name=brand_name_2)

        if not result_1 or not result_2:
            raise HTTPException(status_code=404, detail="Không tìm thấy một hoặc cả hai thương hiệu trong CSDL.")

        def process_result(result):
            for item in result:
                item["brand_data_llm"] = json.loads(item["brand_data_llm"])
                item["comment_data_llm"] = json.loads(item["comment_data_llm"])

                item["brand_data_llm"]["danh_sach_tu_tot"] = ast.literal_eval(item["brand_data_llm"]["danh_sach_tu_tot"].replace("\\\"", "\"").replace("\\'", "'"))
                item["brand_data_llm"]["danh_sach_tu_xau"] = ast.literal_eval(item["brand_data_llm"]["danh_sach_tu_xau"].replace("\\\"", "\"").replace("\\'", "'"))
                item["comment_data_llm"]["danh_sach_tu_tot"] = ast.literal_eval(item["comment_data_llm"]["danh_sach_tu_tot"].replace("\\\"", "\"").replace("\\'", "'"))
                item["comment_data_llm"]["danh_sach_tu_xau"] = ast.literal_eval(item["comment_data_llm"]["danh_sach_tu_xau"].replace("\\\"", "\"").replace("\\'", "'"))
            return result

        # Xử lý dữ liệu
        processed_result_1 = process_result(result_1)
        processed_result_2 = process_result(result_2)

        return DanhGia(
            id="chatbot-response-compare",
            data=[{"brand": brand_name_1, "data_brand1": processed_result_1}, {"brand": brand_name_2, "data_brand2": processed_result_2}]
        )

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
    