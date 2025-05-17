import threading

from fastapi import FastAPI
from app.routers import base, file_upload, crawl, danh_gia_thuong_hieu
from fastapi.middleware.cors import CORSMiddleware

from app.utils.crawl_worker import crawl_worker

# Tạo instance của FastAPI
app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả nguồn (hoặc chỉ định danh sách ["http://example.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả headers
)

# Include các router vào ứng dụng chính
app.include_router(base.router)
app.include_router(crawl.router)
# app.include_router(file_upload.router)
app.include_router(danh_gia_thuong_hieu.router)

# @app.route("/favicon.ico")
# def favicon():
#     return "", 204

# Khi chạy ứng dụng FastAPI
threading.Thread(target=crawl_worker, daemon=True).start()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application"}


