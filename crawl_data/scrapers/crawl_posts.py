#Improt Modules
from crawl_data.utils.login import FacebookLogin
from crawl_data.scrapers.crawl_comment import CrawlComment


# imprt thư viện của selenim
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException

import pandas as pd
from time import sleep
import random



class CrawlPost:
    def __init__(self, driver: WebDriver, cookies_file: str, word_search: str):
        # Khởi tạo các thuộc tính cần thiết
        self.driver = driver
        self.cookies_file = cookies_file
        self.word_search = word_search

        # Xpath của phần post 
        self.xpath_post_link = "//a[contains(@href, '/posts/')]"
        # self.xpath_post_content = "//div[@data-testid='post_body']"

        # Xpath của phần cào comment fanpages
        self.xpath_button_comment = "//div[@role='button' and @id and contains(., 'bình luận')]"
        self.button_close = "//div[@aria-label='Đóng'and @role = 'button']"
        self.posts_element = "//div[@aria-posinset and @aria-describedby]"

    # def clean_data(self, df):
    #     df = df.drop_duplicates(subset="post_id")
    #     return df
    
    def crawl_comment_groups_by_post(self, group_file: str, quantity: int ):
        """ Crawl danh sách post_id từ group Facebook """
        # Đọc danh sách group_id từ file CSV
        df = pd.read_csv(group_file)
        group_urls = df["group_url"].tolist()

        # Danh sách lưu ID bài viết
        comments = []
        stop_crawling = False

        # Lặp qua từng group để lấy bài viết
        isLogin = FacebookLogin(driver=self.driver,
                            cookie_path=self.cookies_file).login_with_cookies()
        
        for i, url in enumerate(group_urls):
            if not isLogin:
                print(f"❌ Không thể đăng nhập fanpage {url}")
                continue

            print("✅ Vào groups:", i)
            self.driver.get(url + f"search/?q={self.word_search}")

            comment_check = []
            sleep(random.uniform(3, 5))

            for scroll_time in range(10):
                if stop_crawling:
                    break

                print(f"🔄 Cuộn trang load bài viết lần {scroll_time}")
                sleep(random.uniform(5, 7))     
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(random.uniform(5, 7))     
                
                try:
                    link_element = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_all_elements_located((By.XPATH, self.xpath_button_comment))
                    )
                    for idx, link in enumerate(link_element):
                        if stop_crawling:
                            break
                        try:
                            # Kiểm tra link có còn trong DOM không
                            self.driver.execute_script("return arguments[0].offsetParent !== null;", link)
                        except StaleElementReferenceException:
                            print(f"❌ Link {idx} không còn trong DOM (StaleElementReferenceException).")
                            continue
                        except Exception as e:
                            print(f"❌ Lỗi khi kiểm tra link {idx}: {e}")
                            continue

                        self.driver.execute_script("arguments[0].scrollIntoView();", link)
                        self.driver.execute_script("arguments[0].click();", link)
                        print("đã click vào: ", link.text)
                        sleep(random.uniform(4, 6))
                        print("Bắt đầu crawl comments")
                        comment_data = CrawlComment(driver=self.driver, cookies_file=self.cookies_file).crawl_comment(brand_name=self.word_search, isgroup=True)
                        
                        if comment_data:
                            print(f"✅ Lấy xong bài post thứ: {idx}")
                            comments.extend(comment_data)
                            comment_check.append(1)
                            print("Comment check" , len(comment_check))     
                        if len(comment_check) >= quantity:
                            stop_crawling = True
                            break         
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException) as e:
                    print(f"❌ Bài viết {idx} không có bình luận hoặc lỗi", e)
                    continue
                except Exception as e:
                    print(f"Lỗi không xác định khi xử lý bài post {idx}")
                    continue
        return pd.DataFrame(comments)


    """Hàm này dùng để lấy comment dựa trên bài post của fanpages"""
    def crawl_comment_fanpages_by_post(self, fanpages_file: str, quantity: int):
        
        df = pd.read_csv(fanpages_file)
        fanpage_urls = df["fanpage_url"].tolist()
        comments = []
        comment_check = []
        stop_crawling = False

        for i, url in enumerate(fanpage_urls):
            isLogin = FacebookLogin(driver=self.driver, cookie_path=self.cookies_file).login_with_cookies()
            if not isLogin:
                print(f"❌ Không thể đăng nhập fanpage {url}")
                continue

            print("✅ Vào fanpage:", i)
            self.driver.get(url)
            sleep(random.uniform(3, 5))

            for scroll_time in range(20):
                if stop_crawling:
                    break

                print(f"🔄 Cuộn trang load bài viết lần {scroll_time}")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                sleep(random.uniform(5, 10))     
                try:
                    link_element = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_all_elements_located((By.XPATH, self.xpath_button_comment))
                    )
                    for idx, link in enumerate(link_element):
                        if stop_crawling:
                            break
                        try:
                            # Kiểm tra link có còn trong DOM không
                            self.driver.execute_script("return arguments[0].offsetParent !== null;", link)
                        except StaleElementReferenceException:
                            print(f"❌ Link {idx} không còn trong DOM (StaleElementReferenceException).")
                            continue
                        except Exception as e:
                            print(f"❌ Lỗi khi kiểm tra link {idx}: {e}")
                            continue

                        self.driver.execute_script("arguments[0].scrollIntoView();", link)
                        self.driver.execute_script("arguments[0].click();", link)
                        print("đã click vào: ", link.text)
                        sleep(random.uniform(4, 6))
                        print("Bắt đầu crawl comments")
                        comment_data = CrawlComment(driver=self.driver, cookies_file=self.cookies_file).crawl_comment(brand_name=self.word_search, isfanpage=True)
                        
                        if comment_data:
                            print(f"✅ Lấy xong bài post thứ: {idx}")
                            comments.extend(comment_data)
                            comment_check.append(1)
                            print("Comment check" , len(comment_check))     
                        if len(comment_check) >= quantity:
                            stop_crawling = True
                            break         
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException) as e:
                    print(f"❌ Bài viết {idx} không có bình luận hoặc lỗi", e)
                    continue
                except Exception as e:
                    print(f"Lỗi không xác định khi xử lý bài post {idx}")
                    continue
        return pd.DataFrame(comments)
    def run(self):
        """ Chạy tất cả các quá trình """
        self.crawl_post_id()
        self.driver.quit()