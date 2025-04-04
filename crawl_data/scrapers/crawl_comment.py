import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException,TimeoutException
import random
from time import sleep
from datetime import date
import random


class CrawlComment:
    def __init__(self, driver: WebDriver, cookies_file:str):
        self.driver = driver
        self.cookies_file = cookies_file
        self.section_comment_xpath = "//div[@role='article' and @aria-label]"
        self.comment_xpath = "./div[2]/div[1]/div[1]"
        self.date_comment_xpath = "./div[2]/div[last()]/ul/li[1]"
        self.button_close = "//div[@aria-label='Đóng'and @role = 'button']"
        self.button_see_more = '//div[@role="button" and contains(text(), "Xem thêm")]'
        # self.scroll_element = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]"
        self.post_popup_xpath = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div"

    def crawl_comment_fanpage(self, brand_name: str):
        comments_file = []
        try:
            while True:
                post_popup = self.driver.find_element(By.XPATH, self.post_popup_xpath)
                last_comments = post_popup.find_elements(By.XPATH, self.section_comment_xpath)

                if len(last_comments) > 1:
                    print("cuộn comment")
                    self.driver.execute_script("arguments[0].scrollIntoView();", last_comments[-1])

                sleep(random.uniform(2, 4))
                new_comments = post_popup.find_elements(By.XPATH, self.section_comment_xpath)

                print(len(last_comments), len(new_comments))
                if len(new_comments) == len(last_comments):
                    try:
                        see_more_buttons = WebDriverWait(post_popup, 5).until(
                                EC.presence_of_all_elements_located((By.XPATH, self.button_see_more))
                            )
                        for see_more_button in see_more_buttons:
                            see_more_button.click()
                            sleep(random.uniform(1, 3))
                    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                        pass
                    
                    for new_comment in new_comments:
                        try:
                            comment_element = new_comment.find_element(By.XPATH, self.comment_xpath)
                            date_comment_element = new_comment.find_element(By.XPATH, self.date_comment_xpath)
                            
                            sleep(random.uniform(1, 3))
                            comments_file.append({
                                "brand_name": brand_name,
                                "comment": comment_element.text.strip(),
                                "date_comment": date_comment_element.text.strip(),
                                "date_crawled": date.today().strftime("%d/%m/%Y"),
                                "data_llm": ""
                            })
                        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                            print(e)
                            continue
                    break
            print("✅ Đã lấy toàn bộ bình luận.")
        except NoSuchElementException as e:
            print("⚠️ Bài viết không có comment")
            sleep(random.uniform(1, 3))
            print(e)
            comments_file.append({
                "brand_name": brand_name,
                "comment": "No comment",
                "date_comment": "",
                "date_crawled": date.today().strftime("%d/%m/%Y"),
                "data_llm": ""
            })
            return comments_file
        finally:
            print("Đợi từ 1 đến 2S và click vào nút close")
            sleep(random.uniform(1, 2))
            try:
                close_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, self.button_close))
                )
                close_button.click()
                sleep(random.uniform(1, 3))
            except TimeoutException:
                print("⚠️ Không tìm thấy nút đóng popup")
                sleep(random.uniform(1, 3))
        return comments_file
        