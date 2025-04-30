from crawl_data.services.crawl_comments_groups import CrawlCommentGroup
from crawl_data.services.crawl_comments_fanpage import CrawlCommentFanpage

chrome_driver_path = "crawl_data\chrome_driver\chromedriver.exe"
cookies_file = "crawl_data\data\cookies\my_cookies.pkl"
word_search = "mv"
list_url = ["https://www.facebook.com/groups/1616819155235042/"]

fanpage_urls = ["https://www.facebook.com/yunbray"]


quantity_fanpages = 1
quantity_post_of_fanpage = 2

# crawler = CrawlCommentGroup(word_search=word_search, 
#                             chrome_driver_path=chrome_driver_path, 
#                             list_url_group = list_url,
#                             cookies_file=cookies_file)

crawler = CrawlCommentFanpage(word_search=word_search,
                    chrome_driver_path=chrome_driver_path, cookies_file=cookies_file, fanpage_urls=fanpage_urls)
file_save = crawler.crawl()
crawler.close()