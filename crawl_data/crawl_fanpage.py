from scrapers.crawl_fanpage import CrawlFanPage
from utils.driver import Driver
from utils.find_filename_by_keyword import find_files_by_keyword

# tham số trong options user_agents

# Khởi tạo driver
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
cookies_file = "crawl_data\data\cookies\my_cookies.pkl"
driver = Driver(chrome_driver_path="crawl_data\chrome_driver\chromedriver.exe",
                user_agent=user_agent, headless=False).get_driver()

# path to the save post file
word_search = "Milo"
folder_path_fanpage = "crawl_data/data/fanpages/"

save_post_file = "crawl_data\data\posts\post.csv"

save_fanpage_file = f"crawl_data\data\\fanpages\{word_search.lower()}.csv"

#check xem word_search_group có trong dữ liệu chưa nếu chưa thì chạy crawlfanpage còn có rồi thì in ra đã có dữ liệu
if not find_files_by_keyword(folder_path=folder_path_fanpage, keyword=word_search):
    # Crawl group
    CrawlFanPage(driver=driver, cookies_file=cookies_file).crawl_fanpage_url(
        quantity=10,
        output_file=save_fanpage_file, 
        word_search=word_search.lower())
else:
    print(f"{word_search} đã có dữ liệu.")
    driver.quit()