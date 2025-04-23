from danh_gia_thuong_hieu.utils.danh_gia_tot_xau import DanhGiaTotXau

# Sử dụng
if __name__ == "__main__":
    comment_file = "crawl_data/data/comments/mái ấm gia đình việt.csv"
    DanhGiaTotXau().run_review(comment_file=comment_file)