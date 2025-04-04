import pandas as pd
from chatbot.services.evaluate_good_bad import EvaluateGoodBad
from time import sleep
import json

# Đọc file CSV
df = pd.read_csv("crawl_data/data/comments/bách hoá xanh.csv")  # Thay "comments.csv" bằng đường dẫn file của bạn

# Giả sử cột chứa comment là "comment"
results = []

for idx, comment in enumerate(df["comments"][:5]):
    print(idx)
    chat = EvaluateGoodBad().get_workflow().compile().invoke(
        input={"question": comment}
    )
    response = chat["generation"]
    sleep(3)
    # Lưu kết quả vào danh sách
    results.append({"comment": comment, "evaluation": response.json()})

# Chuyển thành DataFrame để dễ xử lý
df_results = pd.DataFrame(results)

# Xuất kết quả ra file CSV mới
df_results.to_csv("evaluated_comments.csv", index=False)

print("Đánh giá hoàn tất! Kết quả được lưu vào evaluated_comments.csv")
