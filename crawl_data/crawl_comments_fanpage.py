from scrapers.crawl_fanpage import CrawlFanPage
from scrapers.crawl_posts import CrawlPost
from utils.driver import Driver
from utils.find_filename_by_keyword import find_files_by_keyword
from time import sleep
import random


class CrawlCommentFanpage:
    def __init__(self, word_search: str, chrome_driver_path: str, cookies_file:str, quantity_fanpages:int, user_agent: str):
        self.word_search = word_search.lower().strip()
        self.cookies_file = cookies_file
        self.quantity_fanpages = quantity_fanpages
        # Khởi tạo driver

        self.driver = Driver(
            chrome_driver_path=chrome_driver_path,
            headless=False,
            user_agent=user_agent,
        ).get_driver()
        
        # Định nghĩa các đường dẫn
        self.folder_fanpages_save_file = "crawl_data/data/fanpages/"
        self.folder_comments_save_file = "crawl_data/data/comments/"
        self.save_fanpages_file = f"crawl_data/data/fanpages/{self.word_search}.csv"
        self.save_comment_file = f"crawl_data/data/comments/{self.word_search}.csv"
    def clean_data(self, df):
        return df.drop_duplicates()
    
    def crawl(self):
        # Kiểm tra xem có dữ liệu nhóm và bình luận đã tồn tại hay không
        matching_files_fanpages = find_files_by_keyword(self.folder_fanpages_save_file, self.word_search)
        matching_files_comments = find_files_by_keyword(self.folder_comments_save_file, self.word_search)
        
        if not matching_files_fanpages:
            print("không tìm thấy file có sẳn")
            # Crawl group

            CrawlFanPage(driver=self.driver, cookies_file=self.cookies_file).crawl_fanpage_url(
                quantity=self.quantity_fanpages, output_file=self.save_fanpages_file, word_search=self.word_search
            )    
            sleep(random.uniform(3, 5))
            #cào comment trong fanpage tại đây
            comment_df = CrawlPost(
                driver=self.driver, cookies_file=self.cookies_file, word_search=self.word_search
            ).crawl_comment_fanpages_by_post(fanpages_file=self.save_fanpages_file)

            if not comment_df.empty:
                comment_df = self.clean_data(comment_df)
                comment_df.to_csv(self.save_comment_file, index=False)
                print(f"Đã lưu dữ liệu bình luận vào {self.save_comment_file}")
        else:
            if matching_files_comments:
                print("Sử dụng dữ liệu có sẵn")
            else:
                print("Dùng file fanpages có sẳn đề crawl comments")
                for idx, file in enumerate(matching_files_fanpages):
                    self.save_comment_file = f"crawl_data/data/comments/{self.word_search + str(idx)}.csv"
                    #cào comment trong fanpage tại đây
                    comment_df = CrawlPost(
                        driver=self.driver, cookies_file=self.cookies_file, word_search=self.word_search
                    ).crawl_comment_fanpages_by_post(fanpages_file=file)

                    if not comment_df.empty:
                        comment_df = self.clean_data(comment_df)
                        comment_df.to_csv(self.save_comment_file, index=False)
                        print(f"Đã lưu dữ liệu bình luận vào {self.save_comment_file}")
                    else:
                        print("Không tìm thấy bình luận nào trong pages này")                     
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    chrome_driver_path = "crawl_data\chrome_driver\chromedriver.exe"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
    cookies_file = "crawl_data\data\cookies\my_cookies.pkl"
    word_search = "xiaomi"
    quantity_fanpages = 1

    crawler = CrawlCommentFanpage(word_search=word_search, chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, quantity_fanpages=quantity_fanpages, user_agent=user_agent)
    crawler.crawl()
    crawler.close()