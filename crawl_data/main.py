from scrapers.facebook_comment_crawl import FacebookCommentCrawler
from scrapers.crawl_post_id import FacebookCrawler
from scrapers.crawl_group import CrawlGroup
from utils.driver import Driver
from utils.process_comment import CommentProcessor

# tham số trong options user_agents

# Khởi tạo driver
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
cookies_file = "crawl_data\data\cookies\my_cookies.pkl"
driver = Driver(chrome_driver_path="crawl_data\chrome_driver\chromedriver.exe",
                user_agent=user_agent, headless=False).get_driver()

# path to the save post file
word_search_group = "apple"

save_group_file = f"crawl_data\data\group\{word_search_group}.csv"
save_post_file = "crawl_data\data\posts\post.csv"

# Crawl group
CrawlGroup(driver=driver, cookies_file=cookies_file).crawl_group_url(
    quantity=5, output_file=save_group_file, word_search=word_search_group)

CrawlGroup(driver=driver, cookies_file=cookies_file).join_group(
    group_file=save_group_file)

# # crawl post_id
# FacebookCrawler(driver=driver, cookies_file=cookies_file, group_file="crawl_data\data\group\group.csv").crawl_post_id(
#     output_file=save_post_file)


# cào dữ liệu comments
# list_comments = FacebookCommentCrawler(
#     driver=driver, cookies_file=cookies_file, post_file=save_post_file).crawl_comments()

# # save file .txt
# CommentProcessor().save_comments_to_txt_by_post_content(
#     list_comments, "demo\data_in\comment_4.txt")

# print("Lưu file xong rồi nè!!!!")
# driver.quit()
