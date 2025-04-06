import pandas as pd
from chatbot.services.evaluate_good_bad import EvaluateGoodBad
from time import sleep
import json
import random


def phan_tich_cam_xuc(danh_sach_tu_tot, danh_sach_tu_xau):
    """
    Phân tích cảm xúc từ danh sách từ tốt, xấu

    Args:
        danh_sach_tu_tot (list): Danh sách các từ tốt.
        danh_sach_tu_xau (list): Danh sách các từ xấu.

    Returns:
        - arr_percent: Danh sách tỷ lệ phần trăm của từ tốt, xấu.
    """
    tong_so_tu = len(danh_sach_tu_tot) + len(danh_sach_tu_xau)

    if tong_so_tu == 0:
        return [0, 0], [[], []]  # Tránh lỗi chia cho 0

    ty_le_tot = len(danh_sach_tu_tot) / tong_so_tu * 100
    ty_le_xau = len(danh_sach_tu_xau) / tong_so_tu * 100

    arr_percent = [ty_le_xau, ty_le_tot]

    return arr_percent

def danh_gia_thuong_hieu(comment_file: str):
    danh_sach_tu_tot, danh_sach_tu_xau = [], []
    # Đọc file CSV
    df = pd.read_csv(comment_file)  # Thay "comments.csv" bằng đường dẫn file của bạn
    df.dropna(subset="comment", inplace=True)

    for idx, comment in enumerate(df["comment"][:2]): 
        print(idx) 
        response = EvaluateGoodBad().get_workflow().compile().invoke(
                input={"question": comment}
            )
        sleep(random.uniform(3, 4))
        # Lấy response text
        raw_text = response["generation"]
        raw_text = raw_text.replace("```json","").replace("```", "")

        raw_dict = json.loads(raw_text)
        arr_percent = phan_tich_cam_xuc(raw_dict["tu_tot"], raw_dict["tu_xau"])
        ty_le_tot = arr_percent[1]
        ty_le_xau = arr_percent[0]
        

        data = {
            "danh_sach_tu_tot": str(raw_dict["tu_tot"]),
            "danh_sach_tu_xau": str(raw_dict["tu_xau"]),
            "GPT": {
                "phan_tram_tot": str(ty_le_tot),
                "phan_tram_xau": str(ty_le_xau),
            }
        }

        danh_sach_tu_tot.extend(raw_dict["tu_tot"])
        danh_sach_tu_xau.extend(raw_dict["tu_xau"])

    arr_percent_total = phan_tich_cam_xuc(danh_sach_tu_tot=danh_sach_tu_tot, danh_sach_tu_xau=danh_sach_tu_xau)

    data_total = {
            "danh_sach_tu_tot": str(danh_sach_tu_tot),
            "danh_sach_tu_xau": str(danh_sach_tu_xau),
            "GPT": {
                "phan_tram_tot": str(arr_percent_total[1]),
                "phan_tram_xau": str(arr_percent_total[0]),
            }
        }
    
    print(data_total)

comment_file = "crawl_data/data/comments/bách hoá xanh0_group.csv"
danh_gia_thuong_hieu(comment_file=comment_file)
