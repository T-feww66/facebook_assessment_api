
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

    def crawl_fanpage_url(self, quantity: int = 10, word_search: str=None, output_file: str=None):
        """Crawl dữ liệu từ URL của fanpage Facebook.
        Args:
            quantity (int): Số lượng fanpage cần crawl.
            output_file(str): file save
            word_search (str): Từ khóa tìm kiếm.
        """
        isLogin = FacebookLogin(driver=self.driver, cookie_path=self.cookies_file).login_with_cookies()

        if isLogin:
            sleep(random.uniform(2, 4))
            print(f"Tìm kiếm các fanpage về {word_search}")

            self.driver.get(f"https://www.facebook.com/search/pages/?q={word_search}&locale=vi_VN")
            try:
                scroll_attempts = 0
                collected_names = []
                collected_urls = []

                #cuộn trang 10 lần mỗi lần từ 300 đến 700 px theo scripts
                while len(collected_names) < quantity:
                    scroll_step = random.randint(300, 700)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
                    print("Kéo xuống lần: ", scroll_attempts)
                    sleep(random.uniform(1, 3))

                    fanpage_url_elements = self.driver.find_elements(By.XPATH, self.xpath_fanpage_url)

                    fanpage_name = [fanpage.text for fanpage in fanpage_url_elements]
                    fanpage_url = [fanpage.get_attribute("href") for fanpage in fanpage_url_elements]

                    collected_names.extend(fanpage_name)
                    collected_urls.extend(fanpage_url)

                    scroll_attempts += 1

                fanpage_df = pd.DataFrame({
                    "fanpage_name": collected_names[:quantity],
                    "fanpage_url": collected_urls[:quantity],
                })
                     
                fanpage_df.to_csv(output_file, index=False)
                return fanpage_df
            except (NoSuchElementException, TimeoutException):
                print("hello không tìm thấy phần tử")