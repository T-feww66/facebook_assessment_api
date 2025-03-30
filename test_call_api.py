
import requests
import json


def testfile(api_url, api_key, question):
    url = f"{api_url}base/chat-bot/"
    data = {
        "question": question
    }
    headers = {"API-Key": api_key}

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def cut_json(data):
    start_idx = data.find('{')  # Tìm vị trí bắt đầu của JSON
    end_idx = data.rfind('}')  # Tìm vị trí kết thúc của JSON

    # Cắt chuỗi JSON từ response
    return data[start_idx:end_idx+1]


# Ví dụ sử dụng:
if __name__ == "__main__":
    api_url = "http://localhost:60074/"  # Thay đổi theo URL thực tế của API
    api_key = "g8ffzq0R5hXGW38ZMSy1sWXVD3hKqxaX"
    question = "Samsung"
    result = testfile(api_url, api_key, question)

    data = result["data"]
    # data = cut_json(data=data)
    

    # data = json.loads(data)

    print(data)
