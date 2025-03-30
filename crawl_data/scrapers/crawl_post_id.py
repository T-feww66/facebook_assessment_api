import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from time import sleep
import random
from utils.login import FacebookLogin


class FacebookCrawler:
    def __init__(self, driver=None, cookies_file=None, group_file=None):
        # Khởi tạo các thuộc tính cần thiết
        self.driver = driver
        self.cookies_file = cookies_file
        self.group_file = group_file

    def crawl_post_id(self, output_file):
        """ Crawl danh sách post_id từ group Facebook """
        # Đọc danh sách group_id từ file CSV
        df = pd.read_csv(self.group_file)
        group_urls = df["group_url"].tolist()

        # Danh sách lưu ID bài viết
        posts = []

        # Lặp qua từng group để lấy bài viết
        for url in group_urls:

            if FacebookLogin(driver=self.driver,
                             cookie_path=self.cookies_file).login_with_cookies():
                
                self.driver.get(url)

                
                post_links = []

                # Cuộn trang để load thêm bài viết
                for i in range(20):
                    print("Kéo xuống lần: ", i)
                    self.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    sleep(random.randint(1, 8))

                    # Tìm tất cả các thẻ <a> chứa link bài viết
                    post_path = "//a[contains(@href, '/posts/')]"
                    class_name = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx " \
                        "xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xkrqix3 x1sur9pj xi81zsa x1s688f"

                    try:
                        # Chờ đến khi phần tử xuất hiện
                        elements = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, post_path))
                            or
                            EC.presence_of_all_elements_located(
                                (By.CLASS_NAME, class_name))
                        )

                        post_links.extend([element.get_attribute("href")
                                           for element in elements])

                    except NoSuchElementException:
                        print(f"Không tìm thấy element này")
                    except TimeoutException:
                        print(f"Không tìm thấy element này")
                    except StaleElementReferenceException:
                        print(f"phần tử thao tác không hợp lệ")

                # lay post tu link va chuyen sang file csv
                if post_links:
                    for i, url_post in enumerate(post_links):
                        url_post = url_post.split("?")[0]
                        post_id = url_post.split("/")[-2]  # Lấy post_id từ URL
                        posts.append(
                            {"post_id": post_id, "post_url": url_post})
                        print(f"Lấy post thứ {i} có URL")
                else:
                    print(f"Không tìm thấy bài viết trong group {url}")

        # Lưu danh sách bài viết vào file CSV
        df_url_posts = pd.DataFrame(posts)
        df_url_posts.to_csv(output_file, index=False)

        print("✅ Đã lấy xong ID bài viết!")
        self.driver.quit()

    def visit_groups(self):
        self.df = pd.read_csv(self.file_group_id)
        group_urls = self.df["group_url"].tolist()

        for index, url in enumerate(group_urls):
            print(str(index) + "->>>>>>> Truy cập group: ", url)

            isLogin = FacebookLogin(driver=self.driver, cookie_path=self.cookies_file).login_with_cookies(
                cookies_file=self.cookies_file, driver=self.driver)
            if isLogin:
                self.driver.get(url)
                sleep(random.randint(1, 8))

    def run(self):
        """ Chạy tất cả các quá trình """
        # self.visit_groups()
        self.crawl_post_id()
        self.driver.quit()

# # Khởi tạo đối tượng và chạy
# chrome_driver_path = "./chromedriver.exe"
# cookies_file = "my_cookies.pkl"
# file_group_id = "./group_id.csv"
# crawler = FacebookCrawler(chrome_driver_path, cookies_file, file_group_id)
# crawler.run()
