import pickle
from time import sleep
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.driver import Driver


class FacebookLogin:
    def __init__(self, driver, cookie_path):
        self.driver = driver
        self.cookie_path = cookie_path

    def send_keys_randomly(self, element, text):
        """Nhập ký tự vào ô input với độ trễ ngẫu nhiên để tránh bị phát hiện là bot."""
        for char in text:
            element.send_keys(char)
            sleep(random.uniform(0.1, 0.5))

    def login_with_credentials(self, email, password, save_cookies=True):
        """Đăng nhập Facebook bằng email và mật khẩu."""
        self.driver.get("https://www.facebook.com")
        sleep(5)

        try:
            user_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "pass")

            self.send_keys_randomly(user_input, email)
            sleep(random.uniform(3, 7))
            self.send_keys_randomly(password_input, password)

            password_input.send_keys(Keys.ENTER)
            sleep(4)  # Chờ trang tải

            if save_cookies:
                pickle.dump(self.driver.get_cookies(),
                            open(self.cookie_path, "wb"))
                print(f"Cookies đã được lưu tại: {self.cookie_path}")
        except Exception as e:
            print(f"Lỗi khi đăng nhập: {e}")

        finally:
            self.driver.quit()

    def login_with_cookies(self):
        """Đăng nhập Facebook bằng cookies."""
        if "facebook.com" not in self.driver.current_url:
            self.driver.get("https://www.facebook.com")
            sleep(random.randint(1, 8))

        print("Đăng nhập bằng cookies nè anh Long")
        try:
            cookies = pickle.load(open(self.cookie_path, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            print("Đăng nhập thành công bằng cookies")
            return True
        except FileNotFoundError:
            print("Không tìm thấy file cookies")


# # Gọi hàm login
# if __name__ == "__main__":
#     chrome_driver_path = "./chrome_driver/chromedriver.exe"
#     driver = Driver(chrome_driver_path=chrome_driver_path).create_driver()

#     fb_login = FacebookLogin(driver)
#     fb_login.login_with_credentials(
#         email="tthai9123456@gmail.com", password="0123456789099")
