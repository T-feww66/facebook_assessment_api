# File cấu hình chung cho ứng dụng

import os
from dotenv import load_dotenv

# Load các biến môi trường từ file .env
load_dotenv()


class Settings:
    # SETTING

    # Thiết lập đường dẫn thư mục gốc của dự án

    """
    Lớp cấu hình chung cho ứng dụng, quản lý các biến môi trường.

    Attributes:
        DIR_ROOT (str): Đường dẫn thư mục gốc của dự án.
    """

    DIR_ROOT = os.path.dirname(os.path.abspath(".env"))
    
    # API KEY
    API_KEY = os.getenv("API_KEY")
    
    KEY_API_GPT = os.environ["KEY_API_GPT"]
    OPENAI_LLM = os.environ["OPENAI_LLM"]

    KEY_API_GEMINI = os.environ["KEY_API_GEMINI"]
    
    NUM_DOC = os.environ["NUM_DOC"]
    
    LLM_NAME = os.environ["LLM_NAME"]
    
    GOOGLE_LLM = os.environ["GOOGLE_LLM"]

settings = Settings()
