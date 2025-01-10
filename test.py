import requests
import json

# URL của API
url = 'http://127.0.0.1:5000/run_conversation'

# Dữ liệu gửi tới API
data = {
    "message": "Xin chào, bạn khỏe không?"
}

# Gửi yêu cầu POST
response = requests.post(url, json=data)

# Kiểm tra phản hồi
if response.status_code == 200:
    print("Phản hồi từ API:", response.json())
else:
    print("Có lỗi xảy ra:", response.status_code)
