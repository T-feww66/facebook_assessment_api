from pydantic import BaseModel


# Định nghĩa mô hình dữ liệu cho người dùng
class Crawl(BaseModel):
    id: str
    data: str