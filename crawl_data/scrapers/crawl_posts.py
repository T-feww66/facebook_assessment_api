#Improt Modules
from crawl_data.utils.login import FacebookLogin
from crawl_data.scrapers.crawl_comment import CrawlComment


# imprt thư viện của selenim
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException

from database.db.crawl_url_repository import CrawlUrlRepository


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

        # Xpath của phần cào comment fanpages
        self.xpath_button_comment = "//div[@role='button' and @id and contains(., 'bình luận')]"
        self.button_close = "//div[@aria-label='Đóng'and @role = 'button']"
        self.posts_element = "//div[@aria-posinset and @aria-describedby]"

        self.xpath_search = "//div[@aria-label='Tìm kiếm' and @role = 'button']"
        self.xpath_menuitem_search = "//div[@role='menuitem']"
        self.xpath_menu = '//div[contains(@aria-label, "Xem thêm") and @aria-haspopup="menu"]'
        self.input = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div/label/input"
        self.repo = CrawlUrlRepository()
    def send_keys_randomly(self, element, text):
        """Nhập ký tự vào ô input với độ trễ ngẫu nhiên để tránh bị phát hiện là bot."""
        for char in text:
            element.send_keys(char)
            sleep(random.uniform(0.1, 0.3))

    def crawl_comment_groups_by_post(self, quantity: int, list_url_group:list ):
        """ Crawl danh sách post_id từ group Facebook """

        # Danh sách lưu ID bài viết
        comments = []
        idx = None

        # Lặp qua từng group để lấy bài viết
        isLogin = FacebookLogin(driver=self.driver,
                            cookie_path=self.cookies_file).login_with_cookies()
        
        for i, url in enumerate(list_url_group):
            id_url = self.repo.get_id_by_url(link=url)
            
            print(id_url)

            stop_crawling = False
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
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(random.uniform(5, 7))     
                
                try:
                    idx = - 1
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
                            print(f"❌ Lỗi khi kiểm tra link {idx}:")
                            continue

                        self.driver.execute_script("arguments[0].scrollIntoView();", link)
                        self.driver.execute_script("arguments[0].click();", link)
                        print("đã click vào: ", link.text)
                        sleep(random.uniform(2, 3))
                        print("Bắt đầu crawl comments")
                        comment_data = CrawlComment(driver=self.driver, cookies_file=self.cookies_file).crawl_comment_group(word_search=self.word_search, isgroup=True, index=id_url)
                                
                        if comment_data:
                            print(f"✅ Lấy xong bài post thứ: {idx}")
                            comments.extend(comment_data)
                            comment_check.append(1)
                            print("Comment check" , len(comment_check))     
                        if len(comment_check) >= quantity:
                            stop_crawling = True
                            break         
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException) as e:
                    print(f"❌ Bài viết {idx} không có bình luận hoặc lỗi")
                    continue
                except Exception as e:
                    print(f"Lỗi không xác định khi xử lý bài post {idx}")
                    continue
        return pd.DataFrame(comments)



    """Hàm này dùng để lấy comment dựa trên bài post của fanpages"""
    def crawl_comment_fanpages_by_post(self, fanpage_urls: list, quantity: int):   
        comments = []
        idx = None

        isLogin = FacebookLogin(driver=self.driver, cookie_path=self.cookies_file).login_with_cookies()
        for i, url in enumerate(fanpage_urls):

            id_url = self.repo.get_id_by_url(link=url)

            stop_crawling = False
            if not isLogin:
                print(f"❌ Không thể đăng nhập fanpage {url}")
                continue

            print("✅ Vào fanpage:", i)
            self.driver.get(url)
            sleep(random.uniform(3, 5))

            comment_check = []

            try:
                # Thử tìm kiếm trực tiếp
                search_elm = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, self.xpath_search))
                )
                self.driver.execute_script("arguments[0].click();", search_elm)
                sleep(random.uniform(1, 2))

            except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
                try:
                    # Fallback: mở menu và chọn item
                    menu_elm = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, self.xpath_menu))
                    )
                    self.driver.execute_script("arguments[0].click();", menu_elm)
                    sleep(random.uniform(1, 2))

                    menu_item_elm = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, self.xpath_menuitem_search))
                    )
                    self.driver.execute_script("arguments[0].click();", menu_item_elm)
                    sleep(random.uniform(1, 2))

                except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
                    pass  # Cả menu cũng fail thì bỏ qua

            # Dù là nhánh nào, nếu input tồn tại thì xử lý
            try:
                input_elm = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, self.input))
                )
                self.send_keys_randomly(input_elm, self.word_search)
                input_elm.send_keys(Keys.ENTER)

            except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
                pass

            for scroll_time in range(10):
                if stop_crawling:
                    break

                print(f"🔄 Cuộn trang load bài viết lần {scroll_time}")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(random.uniform(5, 7))     
                
                try:
                    idx = - 1
                    link_element = WebDriverWait(self.driver, 5).until(
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
                            print(f"❌ Lỗi khi kiểm tra link {idx}")
                            continue

                        self.driver.execute_script("arguments[0].scrollIntoView();", link)
                        self.driver.execute_script("arguments[0].click();", link)
                        print("đã click vào: ", link.text)
                        sleep(random.uniform(4, 6))
                        print("Bắt đầu crawl comments")
                        comment_data = CrawlComment(driver=self.driver, cookies_file=self.cookies_file).crawl_comment(word_search=self.word_search, isfanpage=True, index=id_url)
                        
                        if comment_data:
                            print(f"✅ Lấy xong bài post thứ: {idx}")
                            comments.extend(comment_data)
                            comment_check.append(1)
                            print("Comment check" , len(comment_check))     
                        if len(comment_check) >= quantity:
                            stop_crawling = True
                            break
                except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException) as e:
                    print(f"❌ Bài viết {idx} không có bình luận hoặc lỗi")
                    continue
                except Exception as e:
                    print(f"Lỗi không xác định khi xử lý bài post {idx}")
                    continue
        return pd.DataFrame(comments)