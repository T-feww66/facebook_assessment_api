from crawl_data.services.crawl_comments_groups import CrawlCommentGroup
from crawl_data.services.crawl_comments_fanpage import CrawlCommentFanpage

chrome_driver_path = "crawl_data\chrome_driver\chromedriver.exe"
cookies_file = "crawl_data\data\cookies\my_cookies.pkl"
word_search = "bác gấu"
quantity_group = 1
quantity_post_of_group = 3

crawler = CrawlCommentFanpage(word_search=word_search, quantity_fanpage=quantity_group,
                              chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, quantity_post_of_fanpage=quantity_post_of_group)
file_save = crawler.crawl()
crawler.close()