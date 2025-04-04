from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
import random


class Driver:
    def __init__(self, chrome_driver_path: str, user_agent: str = "", headless: bool = False, proxy: str = ""):
        """
        Khởi tạo đối tượng Driver.

        Args:
            chrome_driver_path (str): Đường dẫn đến ChromeDriver.
            user_agent (str): User-Agent để tránh bị phát hiện là bot.
            headless (bool): Chạy trình duyệt ở chế độ headless hay không.
            proxy (str): Địa chỉ proxy theo định dạng "IP:PORT".
        """
        self.chrome_driver_path = chrome_driver_path
        self.user_agent = user_agent
        self.headless = headless
        self.proxy = proxy
        self.driver = None

    def create_driver(self) -> WebDriver:
        """
        Khởi tạo trình duyệt với các tùy chọn cấu hình.

        Returns:
            WebDriver: Đối tượng trình duyệt Selenium đã khởi tạo.
        """
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # full screen
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bỏ qua chế độ tự động
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Giảm phát hiện bot 
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-cache")
        
        # Cài đặt proxy nếu có
        if self.proxy:
            chrome_options.add_argument(f"--proxy-server={self.proxy}")

        # Cài đặt user-agent nếu có
        if self.user_agent:
            chrome_options.add_argument(f"--user-agent={self.user_agent}")

        if self.headless:
            chrome_options.add_argument("--headless=new")  # Chạy headless
            chrome_options.add_argument("--disable-gpu")  # Tắt GPU (cần trên Windows)
            print("🚀 Đang chạy trình duyệt ở chế độ HEADLESS")

        # Khởi tạo trình duyệt
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