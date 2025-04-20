from crawl_data.scrapers.crawl_groups import CrawlGroup
from crawl_data.scrapers.crawl_posts import CrawlPost
from crawl_data.utils.driver import Driver
from crawl_data.utils.find_filename_by_keyword import find_files_by_keyword
from time import sleep
import random

class CrawlCommentGroup:
    def __init__(self, word_search: str, name_group: str, chrome_driver_path: str, cookies_file:str, quantity_group:int, quantity_post_of_group: int = 5 ):
        self.word_search = word_search.lower().strip()
        self.cookies_file = cookies_file
        self.quantity_group = quantity_group
        self.quantity_post = quantity_post_of_group
        self.name_group = name_group.lower().strip()
        # Khởi tạo driver
        self.driver = Driver(
            chrome_driver_path=chrome_driver_path,
            headless=True,
        ).get_driver()
        
        # Định nghĩa các đường dẫn
        self.folder_group_save_file = "crawl_data/data/group/"
        self.folder_comments_save_file = "crawl_data/data/comments/"
        self.save_group_file = f"crawl_data/data/group/{self.name_group}.csv"
        self.save_comment_file = f"crawl_data/data/comments/{self.word_search}_group.csv"
        
    def clean_data(self, df):
        df.dropna(subset="comment", inplace=True)
        return df.drop_duplicates()

    def crawl(self):
        # Kiểm tra xem có dữ liệu nhóm và bình luận đã tồn tại hay không
        matching_files_groups = find_files_by_keyword(self.folder_group_save_file, self.name_group)
        matching_files_comments = find_files_by_keyword(self.folder_comments_save_file, self.word_search)

        print(matching_files_comments, matching_files_groups)
        
        if not matching_files_groups:  
            # Crawl group
            CrawlGroup(driver=self.driver, cookies_file=self.cookies_file).crawl_group_url(
                quantity_group=self.quantity_group, output_file=self.save_group_file, name_group=self.name_group
            ) 
            sleep(random.uniform(3, 5))
            # Crawl posts
            comment_df = CrawlPost(
                driver=self.driver, cookies_file=self.cookies_file, word_search=self.word_search
            ).crawl_comment_groups_by_post(group_file=self.save_group_file, quantity=self.quantity_post)
            
            # Làm sạch và lưu dữ liệu
            comment_df = self.clean_data(comment_df)
            comment_df.to_csv(self.save_comment_file, index=False)
            return self.save_comment_file
        else:
            if matching_files_comments:
                print("Sử dụng dữ liệu có sẵn")
                return matching_files_comments[0]
            else:
                for idx, file in enumerate(matching_files_groups):     
                    self.save_comment_file = f"crawl_data/data/comments/{self.word_search + str(idx)}_group.csv"
                    comment_df = CrawlPost(
                        driver=self.driver, cookies_file=self.cookies_file, word_search=self.word_search
                    ).crawl_comment_groups_by_post(group_file=file, quantity=self.quantity_post)
                    
                    comment_df = self.clean_data(comment_df)
                    comment_df.to_csv(self.save_comment_file, index=False)            
                return self.save_comment_file
    
    
    def close(self):
        self.driver.quit()