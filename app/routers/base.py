from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401

from app.models.base import Base

# import file chat agent
from chatbot.services.files_chat_agent import FilesChatAgent
from ingestion.ingestion import Ingestion

from app.api_config import settings

from app.security.security import get_api_key

# Tạo router cho người dùng
router = APIRouter(prefix="/base", tags=["base"])


@router.post("/base-url/", response_model=Base)
async def base_url(
    api_key: str = get_api_key,  # Khóa API để xác thực
    base_data: str = Form(""),
):

    return Base(id="EKcG&@(t|x_8xr/`ObZb|uQ+^'[i_L", data=base_data)


@router.post("/chat-bot/", response_model=Base)
async def chat_bot(
        api_key: str = get_api_key,  # Khóa API để xác thực
        question: str = Form(""),
):
    
    Ingestion(settings.AI).ingestion_folder(
        path_input_folder="demo/data_in",
        path_vector_store="demo/data_vector",
    )

    try:
        # Khởi tạo chatbot với dữ liệu vector đã lưu
        chat = FilesChatAgent("demo/data_vector").get_workflow().compile().invoke(
            input={"question": question}
        )

        # Lấy kết quả chatbot sinh ra
        response = chat["generation"]
        return Base(id="chatbot-response", data=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
    
@router.post("/refresh-settings")
def refresh():
    settings.reload()
    return {"status": "reloaded"}