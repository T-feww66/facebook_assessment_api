from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
import tempfile

class Driver:
    def __init__(self, chrome_driver_path: str, headless: bool = False, proxy: str = ""):
        """
        Khởi tạo đối tượng Driver.

        Args:
            chrome_driver_path (str): Đường dẫn đến ChromeDriver.
            user_agent (str): User-Agent để tránh bị phát hiện là bot.
            headless (bool): Chạy trình duyệt ở chế độ headless hay không.
            proxy (str): Địa chỉ proxy theo định dạng "IP:PORT".
        """
        self.chrome_driver_path = chrome_driver_path
        self.headless = headless
        self.proxy = proxy
        self.driver = None


    def create_driver(self) -> WebDriver:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36")
        chrome_options.add_argument("--window-size=768,1024")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-cache")
        chrome_options.add_argument("--enable-unsafe-swiftshader")
        chrome_options.add_argument("--disable-gpu")

        # Tạo thư mục user-data riêng
        chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

        if self.proxy:
            chrome_options.add_argument(f"--proxy-server={self.proxy}")
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            print("🚀 Đang chạy trình duyệt ở chế độ HEADLESS")

        service = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver


    def get_driver(self) -> WebDriver:
        """
        Lấy driver hiện tại. Nếu chưa có, tự động tạo mới.
        Returns:
            WebDriver: Đối tượng trình duyệt.
        """
        if self.driver is None:
            return self.create_driver()
        return self.driver

    def quit(self):
        """Dừng driver nếu đã khởi tạo"""
        if self.driver:
            self.driver.quit()
            self.driver = None