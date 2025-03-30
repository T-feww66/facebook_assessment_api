from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
import random
from time import sleep
from config import settings
from selenium.webdriver.chrome.webdriver import WebDriver


class FacebookLogin:

    """Class dùng để Login Facebook"""

    def __init__(self, driver: WebDriver, cookie_path: str):
        """
            Khởi tạo đăng nhập facebook

            Args:
                driver (WebDriver): Đối tượng WebDriver đã khởi tạo
                cookie_path (str): Đường dẫn tới file cookies.
        """

        self.driver = driver
        self.cookie_path = cookie_path

    def send_keys_randomly(self, element, text):
        """Nhập ký tự vào ô input với độ trễ ngẫu nhiên để tránh bị phát hiện là bot."""
        for char in text:
            element.send_keys(char)
            sleep(random.uniform(0.1, 0.5))

    def login_with_credentials(self, email: str, password: str, save_cookies: bool = True) -> bool:
        """
        Đăng nhập Facebook bằng email và mật khẩu.

        Args:
            email (str): Email đăng nhập
            password (str): Mật khẩu đăng nhập
            save_cookies (bool): Mô tả việc lưu cookies. Defaults to True.
        """
        self.driver.get("https://www.facebook.com")
        sleep(random.randint(1, 3))

        try:
            user_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "pass")

            self.send_keys_randomly(user_input, email)
            sleep(random.randint(1, 3))
            self.send_keys_randomly(password_input, password)

            password_input.send_keys(Keys.ENTER)
            sleep(random.randint(1, 3))

            if save_cookies:
                pickle.dump(self.driver.get_cookies(),
                            open(self.cookie_path, "wb"))
                print(f"Cookies đã được lưu tại: {self.cookie_path}")
        except Exception as e:
            print(f"Lỗi khi đăng nhập: {e}")

        finally:
            return True

    def login_with_cookies(self) -> bool:
        """Đăng nhập Facebook bằng cookies và kiểm tra xem cookies có hết hạn không."""

        if "facebook.com" not in self.driver.current_url:
            self.driver.get("https://www.facebook.com")
            sleep(random.randint(1, 3))

        try:
            cookies = pickle.load(open(self.cookie_path, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            sleep(5)

            # Kiểm tra nếu đã đăng nhập thành công
            if self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div/div[1]/div[1]/ul"):
                return True
            else:
                return self.login_with_credentials(email=settings.EMAIL, password=settings.PASSWORD)
        except FileNotFoundError:
            return self.login_with_credentials(email=settings.EMAIL, password=settings.PASSWORD)
