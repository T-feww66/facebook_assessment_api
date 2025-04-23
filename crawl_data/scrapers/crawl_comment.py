from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

from crawl_data.utils.convert_date import convert_time_label_to_date
import random
from time import sleep
from datetime import date
import random


class CrawlComment:
    def __init__(self, driver: WebDriver, cookies_file: str):
        self.driver = driver
        self.cookies_file = cookies_file
        self.section_comment_xpath = "//div[@role='article' and @aria-label]"
        self.comment_xpath = "./div[2]/div[1]/div[1]/div/div/div[last()]"
        self.date_comment_xpath = "./div[2]/div[last()]/ul/li[1]"
        self.button_close = "//div[@aria-label='Đóng'and @role = 'button']"
        self.button_see_more = '//div[@role="button" and contains(text(), "Xem thêm")]'
        self.post_popup_xpath = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div"

        self.post_content_xpath_reel = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[1]/div/a/div[1]/div[2]/div/div/div[2]/span/div"
        self.post_content_xpath = "//div[@role='dialog'][@aria-labelledby]//div[@dir='auto']"
        self.see_more_path = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[1]/div/a/div[1]/div[2]/div/div/div[2]/span/div/object/div"

    def crawl_post_content(self):
        try:
            # Thử click "See more" nếu có
            see_more = WebDriverWait(self.driver, random.uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, self.see_more_path))
            )
            see_more.click()
            sleep(random.uniform(1, 3))  # Ngủ vừa đủ sau khi click
        except TimeoutException:
            pass  
        
        # Sau khi click hoặc không có "See more", thử lấy nội dung từ 2 xpath
        for xpath in [self.post_content_xpath, self.post_content_xpath_reel]:
            try:
                post_element = WebDriverWait(self.driver, random.uniform(3, 5)).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                return post_element.text
            except TimeoutException:
                continue

        return "Not found"


    def crawl_comment(self, brand_name: str, isgroup: bool = False, isfanpage: bool = False):
        comments_file = []
        try:
            post_popup = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.post_popup_xpath))
            )
            while True:
                last_comments = WebDriverWait(post_popup, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, self.section_comment_xpath))
                )

                if len(last_comments) >= 1:
                    print("cuộn comment")
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", last_comments[-1])

                sleep(random.uniform(2, 4))
                new_comments = WebDriverWait(post_popup, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, self.section_comment_xpath))
                )
                print(len(last_comments), len(new_comments))
                if len(new_comments) == len(last_comments):
                    try:
                        see_more_buttons = WebDriverWait(post_popup, 5).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, self.button_see_more))
                        )
                        for see_more_button in see_more_buttons:
                            self.driver.execute_script(
                                "arguments[0].click();", see_more_button)
                            sleep(random.uniform(1, 3))
                    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                        pass

                    for new_comment in new_comments:
                        try:
                            comment_element = new_comment.find_element(
                                By.XPATH, self.comment_xpath)
                            date_comment_element = new_comment.find_element(
                                By.XPATH, self.date_comment_xpath)
                            print(date_comment_element.text)
                            comments_file.append({
                                "brand_name": brand_name,
                                "post_content": "",
                                "is_group": 1 if isgroup else 0,
                                "is_fanpage": 1 if isfanpage else 0,
                                "comment": comment_element.text.strip(),
                                "date_comment": convert_time_label_to_date(label=date_comment_element.text, date_now=date.today().strftime("%d/%m/%Y")),
                                "date_crawled": date.today().strftime("%d/%m/%Y"),
                                "data_llm": ""
                            })
                        except Exception as e:
                            continue
                    break
        except Exception as e:
            print("⚠️ Bài viết không có comment hoặc popup")
        finally:
            # Luôn cố gắng đóng popup nếu có thể
            print("Đợi từ 1 đến 2s và cố gắng click nút close popup (nếu có)")
            sleep(random.uniform(1, 2))
            try:
                close_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.button_close))
                )
                close_button.click()
                sleep(random.uniform(1, 3))
                print("✅ Đã xử lý xong bài viết.")
            except TimeoutException:
                print("⚠️ Không tìm thấy nút đóng popup")
                sleep(random.uniform(1, 3))

            return comments_file
        
    def crawl_comment_group(self, brand_name: str, isgroup: bool = False, isfanpage: bool = False):
        comments_file = []
        post_content = self.crawl_post_content()
        try:
            post_popup = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.post_popup_xpath))
            )
            while True:
                last_comments = WebDriverWait(post_popup, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, self.section_comment_xpath))
                )

                if len(last_comments) >= 1:
                    print("cuộn comment")
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", last_comments[-1])

                sleep(random.uniform(2, 4))
                new_comments = WebDriverWait(post_popup, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, self.section_comment_xpath))
                )
                print(len(last_comments), len(new_comments))
                if len(new_comments) == len(last_comments):
                    try:
                        see_more_buttons = WebDriverWait(post_popup, 5).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, self.button_see_more))
                        )
                        for see_more_button in see_more_buttons:
                            self.driver.execute_script(
                                "arguments[0].click();", see_more_button)
                            sleep(random.uniform(1, 3))
                    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                        pass

                    for new_comment in new_comments:
                        try:
                            comment_element = new_comment.find_element(
                                By.XPATH, self.comment_xpath)
                            date_comment_element = new_comment.find_element(
                                By.XPATH, self.date_comment_xpath)
                            print(date_comment_element.text)
                            comments_file.append({
                                "brand_name": brand_name,
                                "post_content": post_content,
                                "is_group": 1 if isgroup else 0,
                                "is_fanpage": 1 if isfanpage else 0,
                                "comment": comment_element.text.strip(),
                                "date_comment": convert_time_label_to_date(label=date_comment_element.text, date_now=date.today().strftime("%d/%m/%Y")),
                                "date_crawled": date.today().strftime("%d/%m/%Y"),
                                "data_llm": ""
                            })
                        except Exception as e:
                            continue
                    break
        except Exception as e:
            print("⚠️ Bài viết không có comment hoặc popup")
        finally:
            # Luôn cố gắng đóng popup nếu có thể
            print("Đợi từ 1 đến 2s và cố gắng click nút close popup (nếu có)")
            sleep(random.uniform(1, 2))
            try:
                close_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.button_close))
                )
                close_button.click()
                sleep(random.uniform(1, 3))
                print("✅ Đã xử lý xong bài viết.")
            except TimeoutException:
                print("⚠️ Không tìm thấy nút đóng popup")
                sleep(random.uniform(1, 3))

            return comments_file
