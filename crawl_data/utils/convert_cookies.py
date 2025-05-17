import pickle

class CookieSaver:
    def __init__(self, cookie_string, domain=".facebook.com", output_file="cookies.pkl"):
        self.cookie_string = cookie_string
        self.domain = domain
        self.output_file = output_file

    def parse_cookies(self):
        cookies = []
        for item in self.cookie_string.strip(";").split(";"):
            try:
                name, value = item.strip().split("=", 1)
                cookie_dict = {
                    "name": name,
                    "value": value,
                    "domain": self.domain,
                    "path": "/",
                    "secure": True,
                    "httpOnly": False,
                }
                cookies.append(cookie_dict)
            except ValueError:
                print(f"⚠️  Bỏ qua cookie không hợp lệ: {item}")
        return cookies

    def save_to_pickle(self):
        cookies = self.parse_cookies()
        with open(self.output_file, "wb") as f:
            pickle.dump(cookies, f)
        print(f"✅ Đã lưu {len(cookies)} cookie vào '{self.output_file}' thành công.")

# # Ví dụ sử dụng:
# if __name__ == "__main__":
#     raw_cookie = (
#         "fr=0rZBfWSDh8uZ6Q08B.AWUytYmAA4Tx0UWrB95zU4Xy9NqsVLJ751khOw.Bn1-dT..AAA.0.0.Bn1-em.AWX1mf-Zxlc; "
#         "c_user=61574237489243; datr=4OcIZzY7xmzl_Ct9AH_TnFgA; xs=39%3ABkS8F7dhYgcDHQ%3A2%3A1742202808%3A-1%3A-1; "
#         "ps_n=1; ps_l=1; wd=430x932; m_pixel_ratio=3; sb=U-fXZ3-C24OY-sdWec02quLE; datr=U-fXZ2XdDWW7Ga8cGbjU0pM2;"
#     )

#     saver = CookieSaver(cookie_string=raw_cookie, output_file="cookies.pkl")
#     saver.save_to_pickle()