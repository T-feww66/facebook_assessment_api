from crawl_data.scrapers.crawl_posts import CrawlPost
from crawl_data.utils.driver import Driver
from crawl_data.utils.find_filename_by_keyword import find_files_by_keyword

class CrawlCommentGroup:
    def __init__(self, word_search: str, chrome_driver_path: str, cookies_file:str, list_url_group:list, quantity_post_of_group: int = 2):
        """
            Khởi tạo đối tượng crawler cho các nhóm Facebook.

            :param word_search: Từ khóa cần tìm trong bài viết.
            :param chrome_driver_path: Đường dẫn đến chromedriver.
            :param cookies_file: Đường dẫn đến file cookies (JSON).
            :param list_url_group: Danh sách URL nhóm Facebook cần crawl.
            :param quantity_post_of_group: Số lượng bài viết sẽ lấy từ mỗi nhóm (mặc định 5).
        """
        self.word_search = word_search.lower().strip()
        self.list_url_group = list_url_group
        self.cookies_file = cookies_file
        self.quantity_post = quantity_post_of_group

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
        comment_df = CrawlPost(
            driver=self.driver, cookies_file=self.cookies_file, word_search=self.word_search
        ).crawl_comment_groups_by_post(quantity=self.quantity_post, list_url_group=self.list_url_group)
        
        comment_df = self.clean_data(comment_df)
        comment_df.to_csv(self.save_comment_file, index=False)            
        return self.save_comment_file
    
    def close(self):
        self.driver.quit()