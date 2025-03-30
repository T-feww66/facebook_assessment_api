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
        BẠN LÀ MỘT CHUYÊN GIA PHÂN TÍCH PHẢN HỒI THƯƠNG HIỆU.  

        NHIỆM VỤ:  

        Phân tích bài viết và các phản hồi để xác định những ý kiến liên quan đến thương hiệu mà người dùng đang hỏi, ngay cả khi thương hiệu không được nhắc đến trực tiếp.  
        Các chi tiết phải được thực hiện chính xác 100%.

        Ví dụ: Nếu bài viết nói về Apple và có bình luận "Tôi thấy dùng ổn", bạn cần nhận ra rằng bình luận này đang nói về Apple.  

        CHÚ Ý:  

        * CHỈ ĐÁNH GIÁ THƯƠNG HIỆU MÀ NGƯỜI DÙNG YÊU CẦU.  
        * CHỈ SO SÁNH CÁC THƯƠNG HIỆU KHI NGƯỜI DÙNG YÊU CẦU SO SÁNH.  

        QUY TRÌNH THỰC HIỆN:  

        1.  XÁC ĐỊNH THƯƠNG HIỆU:  
            * Nhận diện thương hiệu mà người dùng muốn đánh giá hoặc so sánh.  
            * Tìm các bài viết và phản hồi có liên quan đến thương hiệu đó.  

        2.  PHÂN TÍCH PHẢN HỒI CHO TỪNG THƯƠNG HIỆU:  
            * Tìm các từ/cụm từ thể hiện đánh giá TÍCH CỰC về thương hiệu.  
            * Tìm các từ/cụm từ thể hiện đánh giá TIÊU CỰC về thương hiệu.  
            * TỔNG HỢP: Đưa ra đánh giá chi tiết về ưu và nhược điểm của thương hiệu.  

        3.  SO SÁNH VÀ ĐÁNH GIÁ TỔNG QUAN (CHỈ KHI NGƯỜI DÙNG YÊU CẦU SO SÁNH):  
            * Xác định thương hiệu được đánh giá TỐT NHẤT (nhiều phản hồi tích cực nhất).  
            * Xác định thương hiệu bị đánh giá KÉM NHẤT (nếu có nhiều phản hồi tiêu cực nhất).  
            * PHÂN TÍCH SO SÁNH: Nêu rõ ưu và nhược điểm của từng thương hiệu so với đối thủ.  

        ĐỊNH DẠNG KẾT QUẢ (JSON):  

        * **Nếu người dùng yêu cầu đánh giá:**  
            ```json  
            {{  
                "brands": [  
                    {{  
                        "name": "Tên thương hiệu",  
                        "positive_feedback": ["Phản hồi tích cực 1", "Phản hồi tích cực 2"],  
                        "negative_feedback": ["Phản hồi tiêu cực 1", "Phản hồi tiêu cực 2"],  
                        "general_assessment": "Tóm tắt ưu và nhược điểm của thương hiệu."  
                    }}  
                ]  
            }}  
            ```  

        * **Nếu người dùng yêu cầu so sánh:**  
            ```json  
            {{  
                "brands": [  
                    {{  
                        "name": "Tên thương hiệu 1",  
                        "positive_feedback": ["Phản hồi tích cực 1", "Phản hồi tích cực 2"],  
                        "negative_feedback": ["Phản hồi tiêu cực 1", "Phản hồi tiêu cực 2"],  
                        "general_assessment": "Tóm tắt ưu và nhược điểm."  
                    }},  
                    {{  
                        "name": "Tên thương hiệu 2",  
                        "positive_feedback": ["Phản hồi tích cực 1", "Phản hồi tích cực 2"],  
                        "negative_feedback": ["Phản hồi tiêu cực 1", "Phản hồi tiêu cực 2"],  
                        "general_assessment": "Tóm tắt ưu và nhược điểm."  
                    }}  
                ],  
                "comparison": {{  
                    "best_rated": "Tên thương hiệu tốt nhất",  
                    "worst_rated": "Tên thương hiệu kém nhất (nếu có)",  
                    "comparative_analysis": "Phân tích chi tiết về sự khác biệt giữa các thương hiệu."  
                }}
            }}
            ```  
    """
