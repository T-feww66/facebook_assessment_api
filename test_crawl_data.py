from crawl_data.services.crawl_comments_groups import CrawlCommentGroup
from crawl_data.services.crawl_comments_fanpage import CrawlCommentFanpage

chrome_driver_path = "crawl_data\chrome_driver\chromedriver.exe"
cookies_file = "crawl_data\data\cookies\my_cookies.pkl"
word_search = "xiaomi"
name_group = "preview đồ công nghệ"
quantity_group = 1
quantity_post_of_group = 2

quantity_fanpages = 1
quantity_post_of_fanpage = 2

# crawler = CrawlCommentGroup(word_search=word_search, 
#                             name_group=name_group,
#                             chrome_driver_path=chrome_driver_path, 
#                             cookies_file=cookies_file, 
#                             quantity_group=quantity_group,
#                             quantity_post_of_group=quantity_post_of_group)

crawler = CrawlCommentFanpage(word_search=word_search, 
                            chrome_driver_path=chrome_driver_path, 
                            cookies_file=cookies_file, 
                            quantity_fanpage=quantity_fanpages,
                            quantity_post_of_fanpage=quantity_post_of_fanpage)
file_save = crawler.crawl()
crawler.close()