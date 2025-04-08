data = {
        "danh_sach_tu_tot": str(danh_sach_tu_tot),
        "danh_sach_tu_xau": str(danh_sach_tu_xau),
        "GPT": {
            "phan_tram_tot": str(ty_le_tot),
            "phan_tram_xau": str(ty_le_xau),
        },
        "PhoBERT": {
            "phan_tram_tot": str(arr_percent[1]),
            "phan_tram_xau": str(arr_percent[0]),
            "phan_tram_trung_tinh": str(arr_percent[2]),
            "danh_sach_tu_tot": str(arr_keywords[1]),
            "danh_sach_tu_xau": str(arr_keywords[0]),
            "danh_sach_tu_trung_tinh": str(arr_keywords[2]),
        },
        "html": {
            "html_from_good": str(html_from_good),
            "html_bad_word": str(html_bad_word),
        }
    }

    json_string = json.dumps(data, ensure_ascii=False, indent=4)

