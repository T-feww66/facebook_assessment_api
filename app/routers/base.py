from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401

from app.models.base import Base

# import file chat agent
from chatbot.services.files_chat_agent import FilesChatAgent
from ingestion.ingestion import Ingestion

from app.ai_config import settings

from app.security.security import get_api_key

# Tạo router cho người dùng
router = APIRouter(prefix="/base", tags=["base"])


# @router.post("/base-url/", response_model=Base)
# async def base_url(
#     api_key: str = get_api_key,  # Khóa API để xác thực
#     base_data: str = Form(""),
# ):
#     """
#     API base test api.

#     Tham số:
#     - `api_key`: Khóa API dùng để xác thực yêu cầu.
#     - `base_data`: Nội dung dữ liệu test (nếu có).

#     Trả về:
#     - `id`: id của api.
#     - `data`: dữ liệu mà người dùng nhập.

#     """

#     return Base(id="EKcG&@(t|x_8xr/`ObZb|uQ+^'[i_L", data=base_data)


# @router.post("/chat-bot/", response_model=Base)
# async def chat_bot(
#         api_key: str = get_api_key,  # Khóa API để xác thực
#         question: str = Form(""),
# ):
#     """
#         API để gửi câu hỏi và nhận phản hồi có trong documents từ chatbot.

#         Tham số:
#         - `api_key`: Khóa API để xác thực.
#         - `question`: Câu hỏi cần gửi tới chatbot.

#         Trả về:
#         - `id`: Định danh phản hồi (mặc định là "chatbot-response").
#         - `data`: Nội dung phản hồi từ chatbot.

#         API này nhận một câu hỏi và trả về câu trả lời tương ứng từ hệ thống chatbot.
#     """

    
#     Ingestion(settings.AI).ingestion_folder(
#         path_input_folder="demo/data_in",
#         path_vector_store="demo/data_vector",
#     )

#     try:
#         # Khởi tạo chatbot với dữ liệu vector đã lưu
#         chat = FilesChatAgent("demo/data_vector").get_workflow().compile().invoke(
#             input={"question": question}
#         )

#         # Lấy kết quả chatbot sinh ra
#         response = chat["generation"]
#         return Base(id="chatbot-response", data=response)
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
    
@router.post("/refresh-settings")
def refresh():
    """
        API để tải lại cấu hình hệ thống từ tệp cấu hình.

        Tham số:
        - Không có tham số đầu vào.

        Trả về:
        - `status`: Trạng thái sau khi tải lại (ví dụ: "reloaded").

        API này được sử dụng để làm mới các thiết lập hệ thống mà không cần khởi động lại server.
    """
    settings.reload()
    return {"status": "reloaded"}