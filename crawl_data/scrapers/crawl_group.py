from selenium.webdriver.common.by import By

from utils.login import FacebookLogin
from time import sleep
import random
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
# from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd


class CrawlGroup ():

    """Class để cào dữ liệu từ nhóm Facebook."""

    def __init__(self, driver: WebDriver, cookies_file: str) -> None:
        """
            Khởi tạo cào group.

            Args:
                driver (Webdriver): driver Chrome.
                cookies_file (str): Đường dẫn file cookies.
        """
        self.driver = driver
        self.cookies_file = cookies_file  # file cookies

        # Xpath Group
        # xpath group element
        self.xpath_groups_element = "//div[@role='article']"
        # link group
        self.xpath_groups_url = "//a[contains(@href, '/groups/') and @role='presentation']"
        self.xpath_button_join_group = "//div[@role='button' and contains(@aria-label, 'Tham gia nhóm')]"
        # nút đóng
        self.xpath_button_oke = "//div[@role='button' and contains(@aria-label, 'OK')]"
        self.xpath_button_close = "//div[@role='button' and contains(@aria-label, 'Đóng')]"

    def send_keys_randomly(self, element, text):
        """Nhập ký tự vào ô input với độ trễ ngẫu nhiên để tránh bị phát hiện là bot."""
        for char in text:
            element.send_keys(char)
            sleep(random.uniform(0.1, 0.5))

    def get_group(self, quantity: int = 5):
        """Lấy danh sách link nhóm công khai."""
        try:
            scroll_attempts = 0
            collected_names = []
            collected_urls = []
            collected_status = []

            # Tiếp tục cuộn cho đến khi tìm đủ số lượng nhóm công khai
            while len(collected_names) < quantity:
                print("Kéo xuống lần: ", scroll_attempts)
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                sleep(random.uniform(1, 3))

                # Lấy lại danh sách các nhóm sau mỗi lần cuộn
                group_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, self.xpath_groups_element))
                )
                group_urls_element = self.driver.find_elements(
                    By.XPATH, self.xpath_groups_url)

                # Lọc các nhóm có từ "công khai"
                for i in range(len(group_element)):
                    # Lấy toàn bộ text của nhóm
                    full_text = group_element[i].text
                    # Trạng thái vẫn lấy dòng cuối
                    group_status = full_text.split("\n")[-1]
                    group_names = full_text.split("\n")[0]
                    if "công khai" in full_text.lower() and len(collected_names) < quantity:
                        collected_names.append(group_names)  # Lưu toàn bộ text
                        collected_urls.append(
                            group_urls_element[i].get_attribute("href"))
                        collected_status.append(group_status)  # Lưu trạng thái

                scroll_attempts += 1

            sleep(random.uniform(1, 2))

            # Tạo DataFrame từ các nhóm đã lọc
            group_df = pd.DataFrame({
                "group_name": collected_names[:quantity],
                "group_url": collected_urls[:quantity],
                "status": collected_status[:quantity]
            })

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"Lỗi khi lấy nhóm: {str(e)}")
            group_df = pd.DataFrame()

        return group_df

    def crawl_group_url(self, quantity: int,  output_file: str, word_search: str):
        """Crawl dữ liệu từ URL của nhóm Facebook.
            Args:
                quantity (int): Số lượng group cần crawl.
                output_file (str): Đường dẫn file output.
                word_search (str): Từ khóa tìm kiếm.
        """
        isLogin = FacebookLogin(
            driver=self.driver, cookie_path=self.cookies_file).login_with_cookies()

        if isLogin:
            sleep(random.uniform(1, 3))

            print(f"Tìm kiếm các group về {word_search}")

            self.driver.get(
                f"https://www.facebook.com/search/groups/?q={word_search}")

            sleep(random.uniform(1, 3))
            group = self.get_group(quantity=quantity)

        # # Lưu danh sách bài viết vào file CSV
        group.to_csv(output_file, index=False)

        print("✅ Đã lấy xong urls group!")
        sleep(random.uniform(1, 3))
        # self.driver.quit()

    def join_group(self, group_file: str):
        """Tham gia vào các nhóm từ file CSV.
            Args:
                group_file (str): Đường dẫn file CSV chứa danh sách nhóm.
        """
        df = pd.read_csv(group_file)
        group_urls = df["group_url"].tolist()
        group_status = df["status"].tolist()

        # Chech Login
        isLogin = FacebookLogin(
            driver=self.driver, cookie_path=self.cookies_file).login_with_cookies()

        if isLogin:
            for idx, url in enumerate(group_urls):
                if group_status[idx] != "Tham gia":
                    print(f"Bạn đã tham gia group: {url}")
                    continue

                print(f"Tham gia vào group: {url}")
                self.driver.get(url)
                sleep(random.uniform(1, 3))

                # Click vào nút tham gia
                try:
                    join_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, self.xpath_button_join_group)))

                    sleep(random.uniform(1, 3))
                    join_button.click()

                    try:
                        close_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, self.xpath_button_oke)))

                        sleep(random.uniform(1, 3))
                        # click bằng js
                        self.driver.execute_script(
                            "arguments[0].click();", close_button)
                        print(f"Đã gửi yêu cầu đến: {url}")
                        df.loc[df["group_url"] == url,
                               "status"] = "Chờ xác nhận"

                    except (TimeoutException, NoSuchElementException):
                        # set df.status bằng truy cập
                        df.loc[df["group_url"] == url, "status"] = "Truy cập"
                except (TimeoutException, NoSuchElementException):
                    print(
                        f"Đã tham gia group hoặc không tìm thấy tham gia ngay : {url}")
                    continue
        df.to_csv(group_file, index=False)
        self.driver.quit()
