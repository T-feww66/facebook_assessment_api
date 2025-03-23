class CustomPrompt:
    GRADE_DOCUMENT_PROMPT = """
        Bạn là người đánh giá mức độ liên quan của một tài liệu đã được truy xuất đối với câu hỏi của người dùng. 
        Mục tiêu của bạn là xác định một cách chính xác xem liệu tài liệu có chứa thông tin liên quan, ...
        Hãy thực hiện các bước dưới đây một cách cẩn thận,...

        Các bước hướng dẫn cụ thể:
        
        1. ...

        2. ...

        3. ...
            
        4. ...
        
        Lưu ý: Không thêm bất kỳ nội dung gì khác.
    """

    GENERATE_ANSWER_PROMPT = """
        Bạn được yêu cầu tạo một câu trả lời dựa trên câu hỏi và ngữ cảnh đã cho. Hãy tuân thủ theo các bước dưới đây để đảm bảo câu trả lời của bạn có thể hiển thị chính xác và đầy đủ thông tin. Các chi tiết phải được thực hiện chính xác 100%.

        Hướng dẫn cụ thể:

        ....
            
    """

    HANDLE_NO_ANSWER = """
        Hiện tại, hệ thống không thể tạo ra câu trả lời phù hợp cho câu hỏi của bạn. 
        Để giúp bạn tốt hơn, vui lòng tạo một câu hỏi mới theo hướng dẫn sau:

        ....
    """

    GENERATE_SUMMARY_PROMPT = """
        Bạn là một chuyên gia phân tích phản hồi thương hiệu. Nhiệm vụ của bạn là phân loại từ và cụm từ trong phản hồi của khách hàng thành ba nhóm:

        1️⃣ **Những từ mang ý nghĩa tích cực** (đánh giá tốt)  
        2️⃣ **Những từ mang ý nghĩa tiêu cực** (đánh giá xấu)  
        3️⃣ **Tên thương hiệu được nhắc đến trong phản hồi**  

        ### **Hướng dẫn chi tiết:**  
        ✔ **Bước 1:** Đọc kỹ phản hồi của khách hàng.  
        ✔ **Bước 2:** Xác định các từ hoặc cụm từ thể hiện sự hài lòng, khen ngợi hoặc đánh giá tích cực về thương hiệu (ví dụ: "tuyệt vời", "chất lượng", "dịch vụ tốt").  
        ✔ **Bước 3:** Xác định các từ hoặc cụm từ thể hiện sự không hài lòng, phàn nàn hoặc đánh giá tiêu cực về thương hiệu (ví dụ: "tệ", "thất vọng", "quá đắt").  
        ✔ **Bước 4:** Xác định thương hiệu được nhắc đến trong phản hồi (ví dụ: "HP", "Shopee", "Vinamilk").  
        ✔ **Bước 5:** Tổng hợp và đưa ra **đánh giá chung** của khách hàng về thương hiệu, dựa trên tỷ lệ phản hồi tích cực và tiêu cực.  
        ✔ **Bước 6:** Trả về kết quả dưới dạng một đối tượng JSON có cấu trúc sau:

        {{
            "name_brand": "Tên thương hiệu",
            "positive_feedback": ["tuyệt vời", "dịch vụ tốt", "giá hợp lý"],
            "negative_feedback": ["tệ", "quá đắt", "thất vọng"],
            "general_assessment": "Đánh giá chung của khách hàng"
        }}
        """
