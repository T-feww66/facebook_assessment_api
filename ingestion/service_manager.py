from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.ai_config import settings


class ServiceManager:
    """
    Quản lý các dịch vụ liên quan đến embeddings.
    """

    def __init__(self) -> None:
        """
        Khởi tạo ServiceManager.
        """
        pass

    def get_embedding_model(self, embedding_model_name: str):
        """
        Trả về mô hình embeddings tương ứng dựa trên tên mô hình.

        Args:
            embedding_model_name (str): Tên của mô hình embeddings.

        Returns:
            OpenAIEmbeddings | None: Đối tượng OpenAIEmbeddings nếu tìm thấy, ngược lại trả về None.
        """
        embeddings = None
        print("tên mô hinh", embedding_model_name)
        if embedding_model_name == "openai":
            embeddings = OpenAIEmbeddings(openai_api_key=settings.AI_API_KEY)
        elif embedding_model_name == "gemini":
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.AI_API_KEY)
        return embeddings
