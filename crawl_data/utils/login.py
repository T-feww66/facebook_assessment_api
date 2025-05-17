from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pickle
import random
from time import sleep
import os
from app.ai_config import settings

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
        self.domain = ".facebook.com"
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
        print("Đăng nhập bằng tài khoản")
        self.driver.get("https://www.facebook.com/")
        try:
            get_started = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath_button_start))
            )
            get_started.click()
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

            try:
                button_save = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, self.xpath_button_save))
                )
                button_save.click()
                sleep(random.uniform(1, 3))
            except (NoSuchElementException, TimeoutException):
                pass
            
            try:
                WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, self.xpath_button_home))
            )
                print("[✅] Đã đăng nhập.")
                # Lưu cookies
                if save_cookies:
                    pickle.dump(self.driver.get_cookies(), open(self.cookie_path, "wb"))
                    print(f"Cookies đã được lưu tại: {self.cookie_path}")
                return True
            except:
                return False

    def save_cookies_from_string(self, cookie_string):
        cookies = []
        for item in cookie_string.strip(";").split(";"):
            try:
                name, value = item.strip().split("=", 1)
                cookie_dict = {
                    "name": name,
                    "value": value,
                    "domain": self.domain,
                    "path": "/",
                    "secure": True,
                    "httpOnly": False,
                }
                cookies.append(cookie_dict)
            except ValueError:
                print(f"⚠️  Bỏ qua cookie không hợp lệ: {item}")
        with open(self.cookie_path, "wb") as f:
            pickle.dump(cookies, f)
        print(f"[✅] Đã lưu {len(cookies)} cookies vào '{self.cookie_path}'")


    def login_with_cookies(self) -> bool:
        """Đăng nhập Facebook bằng cookies nếu chưa login. Nếu cookie hết hạn thì dùng tài khoản."""

        # Nếu đã đăng nhập thì bỏ qua
        if self.check_login():
            print("[ℹ️] Đã đăng nhập, bỏ qua login.")
            return True

        # Chuyển đến trang login để đảm bảo domain đúng
        if "facebook.com" not in self.driver.current_url:
            self.driver.get("https://www.facebook.com/")
            sleep(random.uniform(1, 3))

        # Không có cookie thì fallback sang login bằng tài khoản
        if not os.path.exists(self.cookie_path):
            print("[!] Không tìm thấy file cookie, sẽ lưu từ settings.COOKIES nếu có.")

            if settings.COOKIES:
                self.save_cookies_from_string(settings.COOKIES)
            else:
                return self.login_with_credentials(settings.EMAIL, settings.PASSWORD)

        try:
            # Thêm cookies
            with open(self.cookie_path, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        print(f"⚠️ Cookie không thể thêm: {cookie['name']} - {e}")

            sleep(random.uniform(1, 2))

            # ⚠️ Dùng refresh thay vì load lại bằng driver.get
            print("[ℹ️] Đang tải lại trang bằng driver.refresh()...")
            self.driver.refresh()
            sleep(random.uniform(2, 4))

            # Nếu có popup lưu thông tin thì click
            try:
                button_save = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, self.xpath_button_save))
                )
                button_save.click()
            except (NoSuchElementException, TimeoutException):
                pass

            # Kiểm tra trạng thái đăng nhập
            if self.check_login():
                print("[✅] Đăng nhập thành công bằng cookie!")
                return True
            else:
                print("[⚠] Cookie hết hạn hoặc không hợp lệ, fallback sang login thường.")
                return self.login_with_credentials(settings.EMAIL, settings.PASSWORD)

        except Exception as e:
            print(f"[❌] Lỗi khi dùng cookies")
            return self.login_with_credentials(settings.EMAIL, settings.PASSWORD)


    
    def check_login(self) -> bool:
        """
        Kiểm tra xem đã đăng nhập thành công hay chưa bằng cách tìm phần tử home.
        """
        try:
            self.driver.get("https://facebook.com/")
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, self.xpath_button_home))
            )
            print("[✅] Đã đăng nhập.")
            return True
        except (NoSuchElementException, TimeoutException):
            return False