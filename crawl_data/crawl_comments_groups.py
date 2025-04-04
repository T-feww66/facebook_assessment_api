from crawl_data.scrapers.crawl_groups import CrawlGroup
from crawl_data.scrapers.crawl_posts import CrawlPost
from crawl_data.utils.driver import Driver
from crawl_data.utils.find_filename_by_keyword import find_files_by_keyword
import os

class CrawlCommentGroup:
    def __init__(self, word_search: str, user_agent:str, chrome_driver_path: str, cookies_file:str, quantity_group:int):
        self.word_search = word_search.lower().strip()
        self.cookies_file = cookies_file
        self.quantity_group = quantity_group
        # Khởi tạo driver
        self.driver = Driver(
            chrome_driver_path=chrome_driver_path,
            user_agent=user_agent,
            headless=False
        ).get_driver()
        
        # Định nghĩa các đường dẫn
        self.folder_group_save_file = "crawl_data/data/group/"
        self.folder_comments_save_file = "crawl_data/data/comments/"
        self.save_group_file = os.path.join(self.folder_group_save_file, f"{self.word_search}.csv")
        self.save_comment_file = os.path.join(self.folder_comments_save_file, f"{self.word_search}.csv")
        
    def clean_data(self, df):
        return df.drop_duplicates()

    def crawl(self):
        # Kiểm tra xem có dữ liệu nhóm và bình luận đã tồn tại hay không
        matching_files_groups = find_files_by_keyword(self.folder_group_save_file, self.word_search)
        matching_files_comments = find_files_by_keyword(self.folder_comments_save_file, self.word_search)
        
        if not matching_files_groups:  
            # Crawl group
            CrawlGroup(driver=self.driver, cookies_file=self.cookies_file).crawl_group_url(
                quantity_group=self.quantity_group, output_file=self.save_group_file, word_search=self.word_search
            ) 
            
            # Crawl posts
            comment_df = CrawlPost(
                driver=self.driver, cookies_file=self.cookies_file, word_search=self.word_search
            ).crawl_comment_by_post(group_file=self.save_group_file)
            
            # Làm sạch và lưu dữ liệu
            comment_df = self.clean_data(comment_df)
            comment_df.to_csv(self.save_comment_file, index=False)
        else:
            if matching_files_comments:
                print("Sử dụng dữ liệu có sẵn")
            else:
                for file in matching_files_groups:
                    comment_df = CrawlPost(
                        driver=self.driver, cookies_file=self.cookies_file, word_search=self.word_search
                    ).crawl_comment_by_post(group_file=file)
                    
                    comment_df = self.clean_data(comment_df)
                    comment_df.to_csv(self.save_comment_file, index=False)
                    
        return self.save_comment_file
    def close(self):
        self.driver.quit()

# if __name__ == "__main__":
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
#     chrome_driver_path = "crawl_data\chrome_driver\chromedriver.exe"
#     cookies_file = "crawl_data\data\cookies\my_cookies.pkl"
#     word_search = "Cà Phê Trung Nguyên Legend"
    
#     crawler = CrawlCommentGroup(word_search, user_agent, chrome_driver_path, cookies_file)
#     crawler.crawl()
#     crawler.close()
