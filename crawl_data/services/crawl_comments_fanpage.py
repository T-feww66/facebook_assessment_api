from crawl_data.scrapers.crawl_fanpage import CrawlFanPage
from crawl_data.scrapers.crawl_posts import CrawlPost
from crawl_data.utils.driver import Driver
from crawl_data.utils.find_filename_by_keyword import find_files_by_keyword
from time import sleep
import random


class CrawlCommentFanpage:
    def __init__(self, word_search: str, chrome_driver_path: str, cookies_file:str, fanpage_urls: list, quantity_post_of_fanpage: int = 2):
        self.word_search = word_search.lower().strip()
        self.cookies_file = cookies_file
        self.fanpage_urls = fanpage_urls
        self.quantity_post = quantity_post_of_fanpage
        # Khởi tạo driver

        self.driver = Driver(
            chrome_driver_path=chrome_driver_path,
            headless=True,
        ).get_driver()
        
        # Định nghĩa các đường dẫn
        self.folder_comments_save_file = "crawl_data/data/comments/"
        self.save_comment_file = f"crawl_data/data/comments/{self.word_search}.csv"

    def clean_data(self, df):
        df.dropna(subset="comment", inplace=True)
        return df.drop_duplicates()
    
    def crawl(self):
        print("Chuẩn bị cào dữ liệu")
        #cào comment trong fanpage tại đây
        comment_df = CrawlPost(
            driver=self.driver, cookies_file=self.cookies_file, word_search=self.word_search
        ).crawl_comment_fanpages_by_post(fanpage_urls= self.fanpage_urls, quantity=self.quantity_post)
        
        if not comment_df.empty:
            comment_df = self.clean_data(comment_df)
            comment_df.to_csv(self.save_comment_file, index=False)
            print(f"Đã lưu dữ liệu bình luận vào {self.save_comment_file}")
        else:
            print("Không tìm thấy bình luận nào trong pages này")      
        return self.save_comment_file               
    
    def close(self):
        self.driver.quit()