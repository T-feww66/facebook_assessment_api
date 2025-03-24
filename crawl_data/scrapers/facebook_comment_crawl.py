import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import random
from time import sleep
from utils.login import FacebookLogin

class FacebookCommentCrawler:
    def __init__(self, driver=None, cookies_file=None, post_file=None):
        self.driver = driver
        self.cookies_file = cookies_file
        self.post_file = post_file
        self.section_comment_xpath = "//div[@role='article']"
        self.post_content_xpath_reel = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[1]/div/a/div[1]/div[2]/div/div/div[2]/span/div"
        self.post_content_xpath = "//div[@role='dialog'][@aria-labelledby]//div[@dir='auto']"
        self.see_more_path = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[1]/div/a/div[1]/div[2]/div/div/div[2]/span/div/object/div"
        self.comment_xpath = "//div[contains(@class, 'xwib8y2') and contains(@class, 'xn6708d') and contains(@class, 'x1ye3gou') and contains(@class, 'x1y1aw1k')]"

    def count_comments(self, xpath):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            return len(elements)
        except:
            return 0

    def crawl_post_content(self):
        try:
            see_more = WebDriverWait(self.driver, random.uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, self.see_more_path)))
            see_more.click()
            sleep(random.uniform(1, 6))
            post_element = WebDriverWait(self.driver, random.uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, self.post_content_xpath_reel)))
            return post_element.text

        except NoSuchElementException:
            post_element = WebDriverWait(self.driver, random.uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, self.post_content_xpath)))
            return post_element.text

        except TimeoutException:
            try:
                post_element = WebDriverWait(self.driver, random.uniform(3, 5)).until(
                    EC.presence_of_element_located((By.XPATH, self.post_content_xpath))
                )
                return post_element.text
            except TimeoutException:
                return None

    def crawl_comments(self):
        comments_file = []
        df = pd.read_csv(self.post_file)
        post_urls = df["post_url"].tolist()[:2]

        for i, post_url in enumerate(post_urls):
            post_id = post_url.split("/")[-2]
            print(f"Truy cập bài viết số: {i}")
            
            if FacebookLogin(self.driver, self.cookies_file).login_with_cookies():
                self.driver.get(post_url)
                sleep(random.uniform(1, 5))
                post_content = self.crawl_post_content()
                
                if post_content:
                    for i in range(10):
                        pre_count_comment = self.count_comments(self.section_comment_xpath)
                        comment_elements = self.driver.find_elements(By.XPATH, self.section_comment_xpath)
                        print(f"Kéo xuống lần: {i}")
                        self.driver.execute_script("arguments[0].scrollIntoView();", comment_elements[-1])
                        sleep(random.randint(3, 6))
                        
                        if self.count_comments(self.section_comment_xpath) == pre_count_comment:
                            print("Đã load toàn bộ bình luận")
                            sleep(random.uniform(1, 4))
                            break
                    
                    try:
                        comment_see_more_xpath = "//div[contains(@class, 'xwib8y2') and contains(@class, 'xn6708d') and contains(@class, 'x1ye3gou') and contains(@class, 'x1y1aw1k')]//div[@role='button']"
                        for see_more_comment in self.driver.find_elements(By.XPATH, comment_see_more_xpath):
                            see_more_comment.click()
                    except (NoSuchElementException, ElementClickInterceptedException):
                        print("Không có bình luận dài hoặc bị che khuất")
                        continue

                    comments = [c.text for c in self.driver.find_elements(By.XPATH, self.comment_xpath)][1:-1]
                    for i_comment, comment in enumerate(comments):
                        print(f"Lấy comment thứ {i_comment}")
                        comment = comment.split("\n")
                        comments_file.append({
                            "post_id": post_id,
                            "post_content": post_content,
                            "username": comment[0],
                            "comment": comment[1]
                        })
                else:
                    comments_file.append({
                        "post_id": post_id,
                        "post_content": post_content,
                        "username": "",
                        "comment": ""
                    })
            else:
                self.driver.quit()
        return comments_file
