# Hệ thống đánh giá thương hiệu dựa trên dữ liệu mạng xã hội Facebook

## Mô tả dự án
Hệ thống đánh giá thương hiệu dựa trên dữ liệu mạng xã hội Facebook bao gồm hai API chính:
- Một API để tự động thu thập (crawl) dữ liệu bình luận từ các bài đăng công khai trên Facebook.
- Một API để đánh giá mức độ cảm xúc tích cực hoặc tiêu cực của từng bình luận thu thập được.

Dự án sử dụng **FastAPI** để xây dựng hệ thống API nhờ tốc độ xử lý nhanh, dễ dàng mở rộng và tích hợp với các công cụ hiện đại.  
Trong quá trình thu thập dữ liệu, **Selenium** được sử dụng để mô phỏng hành vi người dùng nhằm vượt qua các hạn chế của Facebook. Sau khi dữ liệu được thu thập, **LangChain** được sử dụng để phối hợp cùng các mô hình ngôn ngữ lớn (LLM) như **GPT** và **Gemini** để đánh giá cảm xúc của từng bình luận.

**Khó khăn:**  
Quá trình thu thập dữ liệu từ Facebook gặp nhiều thách thức do hạn chế về quyền truy cập và thay đổi giao diện liên tục. Tuy nhiên, việc áp dụng các mô hình ngôn ngữ lớn để đánh giá cảm xúc diễn ra khá suôn sẻ.

**Tính năng trong tương lai:**  
- Phát triển dashboard trực quan hóa thống kê cảm xúc thương hiệu theo thời gian thực.  
- Tự động phát hiện và cảnh báo sớm về khủng hoảng truyền thông (nếu có).  
- Mở rộng hệ thống sang các nền tảng mạng xã hội khác như Instagram, Twitter/X.

## Mục lục
- [Hướng dẫn cài đặt và chạy dự án](#hướng-dẫn-cài-đặt-và-chạy-dự-án)
- [Hướng dẫn sử dụng dự án](#hướng-dẫn-sử-dụng-dự-án)
- [Ghi công và cảm ơn](#ghi-công-và-cảm-ơn)
- [License](#license)

## Hướng dẫn cài đặt và chạy dự án

### Cài đặt Docker
1. **Build Docker image:**
  ```bash
   docker build -t api-base-image .
  ```
2. **Chạy docker container:**
  ```bash
    docker run -d --restart always \
  -v "D:/DNC/thuctapthaykhoi/docker-demo/crawl_data/data":/_app_/crawl_data/data/ \
  -v "D:/DNC/thuctapthaykhoi/docker-demo/crawl_data/chrome_driver/":/_app_/crawl_data/chrome_driver/ \
  --name api-base-container \
  -p 55006:60074 \
  api-base-image
  ```
### Hướng dẫn sử dụng dự án
- Truy cập API docs tại địa chỉ: http://localhost:55006/docs để chạy các API.

- Authentication: Cần truyền mã token: g8ffzq0R5hXGW38ZMSy1sWXVD3hKqxaX

### Ghi công và cảm ơn
- Dự án được phát triển bởi **Trần Thái Trọng**.

- Tài liệu tham khảo:
  - [Selenium Official Documentation](https://www.selenium.dev/)
  - [LangChain Official Documentation](https://www.langchain.com/)
  - [FastAPI Official Documentation](https://fastapi.tiangolo.com/)

### License
- Không có License.