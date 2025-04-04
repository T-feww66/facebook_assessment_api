
from crawl_data.utils.login import FacebookLogin

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import pandas as pd
from time import sleep
import random


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

    def crawl_fanpage_url(self, quantity: int, output_file: str, word_search: str):
        """Crawl dữ liệu từ URL của fanpage Facebook.
        Args:
            quantity (int): Số lượng fanpage cần crawl.
            output_file (str): Đường dẫn file output.
            word_search (str): Từ khóa tìm kiếm.
        """
        isLogin = FacebookLogin(driver=self.driver, cookie_path=self.cookies_file).login_with_cookies()

        if isLogin:
            sleep(random.uniform(2, 4))
            print(f"Tìm kiếm các fanpage về {word_search}")

            self.driver.get(f"https://www.facebook.com/search/pages/?q={word_search}&locale=vi_VN")
            try:

                #cuộn trang 10 lần mỗi lần từ 300 đến 700 px theo scripts
                for _ in range(10):
                    scroll_step = random.randint(300, 700)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
                    sleep(random.uniform(2, 4))

                    fanpage_url_elements = self.driver.find_elements(By.XPATH, self.xpath_fanpage_url)

                    if len(fanpage_url_elements) > quantity:
                        # Lấy thông tin từ danh sách fanpage
                        fanpage_name = [fanpage.text for fanpage in fanpage_url_elements]
                        fanpage_url = [fanpage.get_attribute("href") for fanpage in fanpage_url_elements]

                        fanpage_df = pd.DataFrame({
                            "fanpage_name": fanpage_name[:quantity],
                            "fanpage_url": fanpage_url[:quantity],
                        })
                        break
                # Lưu vào file nếu cần
                if output_file:
                    print("Hoàn Tất")
                    fanpage_df.to_csv(output_file, index=False, encoding="utf-8")
            except (NoSuchElementException, TimeoutException):
                print("hello không tìm thấy phần tử")