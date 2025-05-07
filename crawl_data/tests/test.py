import re

def convert_value(val):
    if not val or val == "Tất cả":
        return None
    val = val.upper().replace(",", ".")
    if "K" in val:
        return int(float(val.replace("K", "")) * 1_000)
    elif "M" in val:
        return int(float(val.replace("M", "")) * 1_000_000)
    else:
        try:
            return int(val)
        except:
            return None

def extract_emotions(data):
    results = []
    for item in data:
        label = item['label']
        value = item['value']

        # Bỏ qua nếu label chứa "Tất cả"
        if "Tất cả" in label:
            continue

        if value == "":
            match = re.search(r"(\d[\d.,]*)", label)
            if match:
                raw_number = match.group(1).replace(".", "").replace(",", "")
                number = int(raw_number)
            else:
                number = 0
        else:
            number = convert_value(value)

        results.append({
            'cam_xuc': label.split("cảm xúc")[-1].strip(),
            'so_luong': number
        })
    return results

# Ví dụ sử dụng
data = [
    {'label': 'Hiển thị 19.538 người đã bày tỏ cảm xúc Tất cả', 'value': ''},
    {'label': 'Hiển thị 0 người đã bày tỏ cảm xúc Thích', 'value': '12K'},
    {'label': 'Hiển thị 0 người đã bày tỏ cảm xúc Yêu thích', 'value': '6,9K'},
    {'label': 'Hiển thị 163 người đã bày tỏ cảm xúc Thương thương', 'value': '163'},
    {'label': 'Hiển thị 50 người đã bày tỏ cảm xúc Haha', 'value': ''},
    {'label': 'Hiển thị 6 người đã bày tỏ cảm xúc Buồn', 'value': ''},
    {'label': 'Hiển thị 5 người đã bày tỏ cảm xúc Wow', 'value': ''},
    {'label': 'Hiển thị 3 người đã bày tỏ cảm xúc Phẫn nộ', 'value': ''}
]

results = extract_emotions(data)

tong = 0
for i in results:
    tong += i["so_luong"]

print(tong)