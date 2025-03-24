from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class Driver:
    def __init__(self, chrome_driver_path, user_agent=None):
        """Khởi tạo đối tượng Driver với các tùy chọn cấu hình"""
        self.chrome_driver_path = chrome_driver_path
        self.user_agent = user_agent
        self.driver = None

    def create_driver(self):
        """Khởi tạo driver với các cấu hình mặc định"""
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  # Giữ lại trình duyệt sau khi script kết thúc
        chrome_options.add_argument("--start-maximized")  # Mở full màn hình
        chrome_options.add_argument("--disable-notifications")  # Tắt thông báo
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bỏ qua chế độ tự động
        
        # Cài đặt user-agent nếu có
        if self.user_agent:
            chrome_options.add_argument(f"--user-agent={self.user_agent}")

        # Khởi tạo trình duyệt
        service = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver

    def quit(self):
        """Dừng driver nếu đã khởi tạo"""
        if self.driver:
            self.driver.quit()
            self.driver = None

# # Sử dụng lớp Driver
# chrome_driver_path = "./chromedriver.exe"
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
# my_driver = Driver(chrome_driver_path=chrome_driver_path, user_agent=user_agent)

# # Khởi tạo driver
# driver = my_driver.create_driver()

# # Thực hiện công việc với driver
# driver.get("https://www.google.com")

# # Sau khi xong, đóng driver
# my_driver.quit()
