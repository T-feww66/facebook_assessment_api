import time
import os
import platform

from app.routers.crawl import crawl_queue
from crawl_data.services.crawl_comments_fanpage import CrawlCommentFanpage
from crawl_data.services.crawl_comments_groups import CrawlCommentGroup  # Bạn cần import class này
from danh_gia_thuong_hieu.utils.danh_gia_tot_xau import DanhGiaTotXau
from database.db.user_send_request_repository import UserSendRequestRepository


# Xác định đường dẫn driver theo hệ điều hành
system = platform.system()
if system == "Windows":
    driver_path = "crawl_data/chrome_driver/chromedriver.exe"
else:
    driver_path = "crawl_data/chrome_driver/chromedriver"


def crawl_worker():
    user_request_repo = UserSendRequestRepository()

    while True:
        if not crawl_queue.empty():
            job = crawl_queue.get()
            print(job)
            try:
                request_id = job["request_id"]
                user_id = job["user_id"]
                word_search = job["word_search"]
                brand_name = job["brand_name"]
                urls = job["crawl_url_link"]
                type = job["type"]

                cookies_file = "crawl_data/data/cookies/my_cookies.pkl"

                if type == 1:
                    # Cào từ fanpage
                    crawler = CrawlCommentFanpage(
                        word_search=word_search,
                        brand_name=brand_name,
                        user_id=user_id,
                        chrome_driver_path=driver_path,
                        cookies_file=cookies_file,
                        fanpage_urls=urls
                    )
                elif type == 0:
                    # Cào từ group
                    crawler = CrawlCommentGroup(
                        word_search=word_search,
                        brand_name=brand_name,
                        user_id=user_id,
                        chrome_driver_path=driver_path,
                        cookies_file=cookies_file,
                        list_url_group=urls
                    )

                file_path = crawler.crawl()
                crawler.close()

                if os.path.exists(file_path):
                    danh_gia = DanhGiaTotXau()
                    danh_gia.run_review(comment_file=file_path, brand_name=brand_name, user_id=user_id)

                    # Cập nhật trạng thái đã xử lý
                    print("request_id", request_id)
                    user_request_repo.update_status_by_id(request_id, 1)
                    print("cập nhật status = 1")
                else:
                    print(f"File {file_path} không tồn tại.")
                    user_request_repo.update_status_by_id(request_id, 2)
                    print("cập nhật status = 1")
            except Exception as e:
                print(f"❌ Error processing job {job['request_id']}: {str(e)}")
        else:
            time.sleep(5)