
import requests
import json

def testfile(api_url, api_key, comment, post_content):
    url = f"{api_url}base/chat-bot/"
    data = {
        "comment": comment,
        "post_content": post_content
    }
    headers = {"API-Key": api_key}
    
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def cut_json (data):
    start_idx = data.find('{')  # Tìm vị trí bắt đầu của JSON
    end_idx = data.rfind('}')  # Tìm vị trí kết thúc của JSON

    # Cắt chuỗi JSON từ response
    return data[start_idx:end_idx+1]


# Ví dụ sử dụng:
if __name__ == "__main__":
    api_url = "http://localhost:60074/"  # Thay đổi theo URL thực tế của API
    api_key = "g8ffzq0R5hXGW38ZMSy1sWXVD3hKqxaX"
    comment = "tôi thấy sài macbook oke hơn đó bạn, tôi thì thấy samsung sài ổn định hơn, sao bạn không chọn redmi tôi đang sài thấy oke lắm á"
    post_content = "Samsum hay là iphone"
    
    result = testfile(api_url, api_key, comment, post_content)

    data = result["data"]
    data = cut_json(data=data)

    data = json.loads(data)
    print(data["general_assessment"])

