import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException, WebDriverException
from time import sleep
import random

from utils.login import FacebookLogin
from scrapers.crawl_comment import CrawlComment


class CrawlPost:
    def __init__(self, driver: WebDriver, cookies_file: str, word_search: str):
        # Khởi tạo các thuộc tính cần thiết
        self.driver = driver
        self.cookies_file = cookies_file
        self.word_search = word_search


        self.xpath_button_comment = "//div[@role='button'and @id]"
        self.button_close = "//div[@aria-label='Đóng'and @role = 'button']"
        self.posts_element = "//div[@aria-posinset and @aria-describedby]"

    # def clean_data(self, df):
    #     df = df.drop_duplicates(subset="post_id")
    #     return df
    

    def crawl_comment_fanpages_by_post(self, fanpages_file: str):
        df = pd.read_csv(fanpages_file)
        group_urls = df["fanpage_url"].tolist()
        comments = []

        for i, url in enumerate(group_urls):
            isLogin = FacebookLogin(driver=self.driver, cookie_path=self.cookies_file).login_with_cookies()
            if not isLogin:
                print(f"❌ Không thể đăng nhập fanpage {url}")
                continue

            print("✅ Vào fanpage:", i)
            self.driver.get(url)
            sleep(random.uniform(3, 5))

            for scroll_time in range(2):
                print(f"🔄 Cuộn trang load bài viết lần {scroll_time}")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(random.uniform(5, 10))
                
                try:
                    link_element = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_all_elements_located((By.XPATH, self.xpath_button_comment))
                    )

                    for idx, link in enumerate(link_element):
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", link)
                        sleep(random.uniform(1, 3))
                        self.driver.execute_script("arguments[0].click();", link)
                        print("đã click vào: ", link.text)

                        sleep(random.uniform(2, 5))
                        print("Bắt đầu crawl comments")
                        comment_data = CrawlComment(driver=self.driver, cookies_file=self.cookies_file).crawl_comment_fanpage(self.word_search)

                        print(f"✅ Lấy xong bài post thứ: {idx}")
                        if comment_data:
                            comments.extend(comment_data)
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException) as e:
                    print(f"❌ Bài viết {idx} không có bình luận hoặc lỗi")
                    continue
                except Exception as e:
                    print(f"Lỗi không xác định khi xử lý bài post {idx}")
                    continue
        return pd.DataFrame(comments)
    def run(self):
        """ Chạy tất cả các quá trình """
        self.crawl_post_id()
        self.driver.quit()