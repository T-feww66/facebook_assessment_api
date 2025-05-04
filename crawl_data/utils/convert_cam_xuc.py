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
