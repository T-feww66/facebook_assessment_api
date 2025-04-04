from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pickle
import random
from time import sleep
import os
from config import settings

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
        self.xpath_button_login = "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button"
        self.xpath_button_home = "/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div/div[1]/div[1]/ul/li[1]/span/div/a"
        self.xpath_button_save = "//div[@aria-label='Lưu' and @role='button']"
        self.xpath_button_start = "//div[@aria-label='Get start' and @role='button']"

    def send_keys_randomly(self, element, text):
        """Nhập ký tự vào ô input với độ trễ ngẫu nhiên để tránh bị phát hiện là bot."""
        for char in text:
            element.send_keys(char)
            sleep(random.uniform(0.1, 0.3))

    def login_with_credentials(self, email: str, password: str, save_cookies: bool = True) -> bool:
        """
        Đăng nhập Facebook bằng email và mật khẩu.
        """
        sleep(random.uniform(1, 3))
        try:
            get_started = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath_button_start))
            )
            get_started.click()
            sleep(random.uniform(1, 3))
        except (NoSuchElementException, TimeoutException):
            # Tìm các phần tử đăng nhập
            user_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "pass"))
            )
            btn_login = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath_button_login))
            )

            # Nhập thông tin đăng nhập
            self.send_keys_randomly(user_input, email)
            sleep(random.uniform(2, 3))
            self.send_keys_randomly(password_input, password)
            sleep(random.uniform(1, 3))

            # Click nút đăng nhập
            btn_login.click()
            sleep(random.uniform(3, 5))

            try:
                button_save = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.xpath_button_save))
                )
                button_save.click()
                sleep(random.uniform(1, 3))
            except (NoSuchElementException, TimeoutException):
                pass

            # Lưu cookies
            if save_cookies:
                pickle.dump(self.driver.get_cookies(), open(self.cookie_path, "wb"))
                print(f"Cookies đã được lưu tại: {self.cookie_path}")
            return True

    def login_with_cookies(self) -> bool:
        """Đăng nhập Facebook bằng cookies và kiểm tra xem cookies có hết hạn không."""

        if "facebook.com" not in self.driver.current_url:
            self.driver.get("https://m.facebook.com/login/")
            sleep(random.randint(1, 3))

        if not os.path.exists(self.cookie_path):
            print("[!] Không tìm thấy file cookie, chuyển sang đăng nhập bằng tài khoản.")
            return self.login_with_credentials(email=settings.EMAIL, password=settings.PASSWORD)

        # Kiểm tra nút "Get Started"
        try:
            get_started = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath_button_start))
            )
            get_started.click()
            sleep(random.uniform(1, 3))
        except (NoSuchElementException, TimeoutException):
            pass  # Nếu không tìm thấy, tiếp tục đăng nhập

        try:
            with open(self.cookie_path, "rb") as f:
                cookies = pickle.load(f)

            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            sleep(random.uniform(2, 8))

            try:
                button_save = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.xpath_button_save))
                )
                button_save.click()
                sleep(random.uniform(1, 3))
            except (NoSuchElementException, TimeoutException):
                pass

            try:
                # Kiểm tra đăng nhập thành công bằng cách tìm một phần tử duy nhất
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.xpath_button_home))
                )
                print("[✅] Đăng nhập thành công bằng cookie!")
                return True
            except (NoSuchElementException, TimeoutException):
                print("[⚠] Cookie hết hạn, cần đăng nhập lại.")
                return self.login_with_credentials(email=settings.EMAIL, password=settings.PASSWORD)

        except Exception as e:
            print(f"[❌] Lỗi khi tải cookie: {e}")
            return self.login_with_credentials(email=settings.EMAIL, password=settings.PASSWORD)