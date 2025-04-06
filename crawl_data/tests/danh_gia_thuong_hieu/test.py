import json

danh_sach_tu_tot = []
danh_sach_tu_xau = []

text = """```json
{"tu_tot": ["ngon"], "tu_xau": ["xl"]}
```"""


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

for i in range(5):
    raw_text = text.replace("```json","").replace("```", "")
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
    # json_string = json.dumps(data, ensure_ascii=False, indent=4)

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