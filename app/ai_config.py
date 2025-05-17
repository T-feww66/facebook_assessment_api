from dotenv import load_dotenv
from database.db.settings_repository import SettingRepository

# settings.py
class Settings:
    def __init__(self):
        self.repo = SettingRepository()
        self.load()

    def load(self):
        self.settings = {row["key"]: row["value"] for row in self.repo.get_all()}
        self.AI = self.settings.get("ai_provider", "")
        self.AI_API_KEY = self.settings.get("ai_api_key", "")
        self.MODEL_LLM = self.settings.get("model_llm", "")
        self.NUM_DOC = self.settings.get("num_doc", "")
        self.COOKIES = self.settings.get("cookies", "")

        # Tài khoản fb
        self.EMAIL = self.settings.get("email", "")
        self.PASSWORD = self.settings.get("password", "")

    def reload(self):
        self.load()

settings = Settings()