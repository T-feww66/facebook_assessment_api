from pydantic import BaseModel
from typing import Union

# Định nghĩa mô hình dữ liệu cho người dùng
class Crawl(BaseModel):
    id: str
    data: Union[str, dict]