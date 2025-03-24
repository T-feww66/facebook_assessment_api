from scrapers.facebook_comment_crawl import FacebookCommentCrawler
from utils.driver import Driver
from utils.process_comment import CommentProcessor

# tham số trong options user_agents
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"

driver = Driver(chrome_driver_path="crawl_data\chrome_driver\chromedriver.exe",
                user_agent=user_agent).create_driver()

list_comments = FacebookCommentCrawler(
    driver=driver, cookies_file="crawl_data\data\cookies\my_cookies.pkl", post_file="crawl_data\data\posts\post_ids_0.csv").crawl_comments()

# save file .txt
CommentProcessor().save_comments_to_txt_by_post_content(
    list_comments, "demo\data_in\comment_0.txt")

print("Lưu file xong rồi nè!!!!")
driver.quit()
