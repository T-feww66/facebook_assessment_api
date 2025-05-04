from danh_gia_thuong_hieu.utils.danh_gia_tot_xau import DanhGiaTotXau

# Sử dụng
if __name__ == "__main__":
    comment_file = "crawl_data/data/comments/7_b ray_the underdog.csv"
    DanhGiaTotXau().run_review(comment_file=comment_file, brand_name="cần thơ", user_id=3 ,limit=20)