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

    # ACCOUNT KEYS
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')


settings = Settings()
