import os
from dotenv import load_dotenv

# Load file .env từ thư mục hiện tại hoặc chỉ định đường dẫn
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

class Settings:
    """
    Lớp cấu hình chung cho ứng dụng, quản lý các biến môi trường.
    """

    # Thiết lập đường dẫn thư mục gốc của dự án
    DIR_ROOT = os.path.dirname(os.path.abspath(__file__))

    # ACCOUNT KEYS
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

settings = Settings()