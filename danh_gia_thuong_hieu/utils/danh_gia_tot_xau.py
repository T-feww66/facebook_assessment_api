import pandas as pd
import json
import random
from time import sleep
from datetime import datetime
from chatbot.services.evaluate_good_bad import EvaluateGoodBad
from database.db.comment_crawl_repository import CommentRepository


class DanhGiaTotXau:
    def __init__(self):
        self.comment_repo = CommentRepository()
        self.evaluator = EvaluateGoodBad()

    def _phan_tich_cam_xuc(self, danh_sach_tu_tot, danh_sach_tu_xau):
        tong_so_tu = len(danh_sach_tu_tot) + len(danh_sach_tu_xau)
        if tong_so_tu == 0:
            return [0, 0]
        ty_le_tot = len(danh_sach_tu_tot) / tong_so_tu * 100
        ty_le_xau = len(danh_sach_tu_xau) / tong_so_tu * 100
        return [ty_le_xau, ty_le_tot]

    def _parse_date(self, date_str):
        try:
            return pd.to_datetime(date_str)
        except Exception:
            return pd.Timestamp.now()

    def run_review(self, comment_file: str, limit: int = None):
        danh_sach_tu_tot = []
        danh_sach_tu_xau = []

        df = pd.read_csv(comment_file)
        if limit:
            df = df.head(limit)

        for idx, row in df.iterrows():
            print(f"Processing comment {idx + 1}/{len(df)}")
            response = self.evaluator.get_workflow().compile().invoke(
                input={"question": row["comment"]}
            )
            sleep(random.uniform(3, 4))

            # Parse response JSON
            raw_text = response["generation"].replace("```json", "").replace("```", "")
            raw_dict = json.loads(raw_text)

            # Phân tích cảm xúc
            arr_percent = self._phan_tich_cam_xuc(raw_dict["tu_tot"], raw_dict["tu_xau"])

            data = {
                "danh_sach_tu_tot": str(raw_dict["tu_tot"]),
                "danh_sach_tu_xau": str(raw_dict["tu_xau"]),
                "GPT": {
                    "phan_tram_tot": str(arr_percent[1]),
                    "phan_tram_xau": str(arr_percent[0]),
                }
            }

            json_string = json.dumps(data, ensure_ascii=False, indent=4)

            # Chuẩn hoá kiểu dữ liệu theo CSDL
            self.comment_repo.insert_crawl_comments_with_data_llm(
                data=json_string,
                brand_name=str(row["brand_name"])[:255],
                is_group=int(row["is_group"]),
                is_fanpage=int(row["is_fanpage"]),
                comment_file=comment_file,
                comment=str(row["comment"]),
                date_comment=str(row["date_comment"]),
                date_crawled=self._parse_date(row["date_crawled"]),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            danh_sach_tu_tot.extend(raw_dict["tu_tot"])
            danh_sach_tu_xau.extend(raw_dict["tu_xau"])

        arr_percent_total = self._phan_tich_cam_xuc(danh_sach_tu_tot=danh_sach_tu_tot, danh_sach_tu_xau=danh_sach_tu_xau)

        data_total = {
                "danh_sach_tu_tot": str(danh_sach_tu_tot),
                "danh_sach_tu_xau": str(danh_sach_tu_xau),
                "GPT": {
                    "phan_tram_tot": str(arr_percent_total[1]),
                    "phan_tram_xau": str(arr_percent_total[0]),
                }
            }
        json_string_total = json.dumps(data_total, ensure_ascii=False, indent=4)

        self.comment_repo.insert_brands_with_data_llm(
            data=json_string_total,
            brand_name=str(df["brand_name"][0]),
            comment_file=comment_file, 
            created_at=datetime.now(),
            updated_at=datetime.now())