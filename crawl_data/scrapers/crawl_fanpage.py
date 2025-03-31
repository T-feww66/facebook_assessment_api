from selenium.webdriver.common.by import By

from utils.login import FacebookLogin
from time import sleep
import random
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

import pandas as pd


class CrawlFanPage ():

    """Class để cào dữ liệu từ fanpage Facebook."""

    def __init__(self, driver: WebDriver, cookies_file: str) -> None:
        """
            Khởi tạo cào fanpage.

            Args:
                driver (Webdriver): driver Chrome.
                cookies_file (str): Đường dẫn file cookies.
        """
        self.driver = driver
        self.cookies_file = cookies_file  # file cookies
        self.xpath_fanpage_url = "//a[contains(@href, '/') and @role='presentation']"

    def get_fanpage(self, quantity: int = 5):
        """Lấy danh sách link các fanpages."""
        try:

            sleep(random.uniform(1, 3))
            # Lấy lại danh sách các nhóm sau mỗi lần cuộn
            fanpage_url_elements = self.driver.find_elements(
                By.XPATH, self.xpath_fanpage_url)

            scroll_attempts = 0
            # Tiếp tục cuộn cho đến khi tìm đủ số lượng pages yêu cầu
            while len(fanpage_url_elements) < quantity:

                print("Kéo xuống lần: ", scroll_attempts)
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                sleep(random.uniform(1, 3))

                # Lấy lại danh sách các nhóm sau mỗi lần cuộn
                fanpage_url_elements = self.driver.find_elements(
                    By.XPATH, self.xpath_fanpage_url)

            fanpage_name = [fanpage.text for fanpage in fanpage_url_elements]
            fanpage_url = [fanpage.get_attribute("href") for fanpage in fanpage_url_elements]

            scroll_attempts += 1

            sleep(random.uniform(1, 2))

            # Tạo DataFrame từ các nhóm đã lọc
            fanpage_df = pd.DataFrame({
                "group_name": fanpage_name[:quantity],
                "group_url": fanpage_url[:quantity],
            })

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"Lỗi khi lấy nhóm: {str(e)}")
            fanpage_df = pd.DataFrame()

        return fanpage_df


    def crawl_fanpage_url(self, quantity: int,  output_file: str, word_search: str):
        """Crawl dữ liệu từ URL của nhóm Facebook.
            Args:
                quantity (int): Số lượng fanpage cần crawl.
                output_file (str): Đường dẫn file output.
                word_search (str): Từ khóa tìm kiếm.
        """
        isLogin = FacebookLogin(
            driver=self.driver, cookie_path=self.cookies_file).login_with_cookies()

        if isLogin:
            sleep(random.uniform(1, 3))

            print(f"Tìm kiếm các fanpage về {word_search}")

            self.driver.get(
                f"https://www.facebook.com/search/pages/?q={word_search}&filters=eyJjYXRlZ29yeTowIjoie1wibmFtZVwiOlwicGFnZXNfY2F0ZWdvcnlcIixcImFyZ3NcIjpcIjEwMDlcIn0ifQ%3D%3D")

            sleep(random.uniform(1, 3))
            fanpage_df = self.get_fanpage(quantity=quantity)

        # # Lưu danh sách bài viết vào file CSV
        fanpage_df.to_csv(output_file, index=False)

        print("✅ Đã lấy xong url fanpages!")
        sleep(random.uniform(1, 3))
        self.driver.quit()