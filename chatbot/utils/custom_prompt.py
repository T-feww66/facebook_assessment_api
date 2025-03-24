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
        Bạn là một chuyên gia phân tích phản hồi thương hiệu. Nhiệm vụ của bạn là phân tích các bình luận để xác định những phản hồi liên quan đến thương hiệu trong bài viết gốc, kể cả khi thương hiệu không được nhắc đến trực tiếp.

        ### **Quy trình thực hiện:**

        1.  **Nhận diện thương hiệu trong bài viết gốc**: Xác định thương hiệu hoặc dịch vụ mà bài viết đề cập đến.
        2.  **Phân loại bình luận**:
            * **Bình luận liên quan**: Nhắc đến thương hiệu (trực tiếp hoặc gián tiếp) hoặc phản hồi về chủ đề trong bài viết.
        3.  **Phân tích phản hồi cho từng thương hiệu**:
            * Xác định **các từ hoặc cụm từ thể hiện đánh giá tích cực** về thương hiệu đó từ bài viết gốc và các bình luận.
            * Xác định **các từ hoặc cụm từ thể hiện đánh giá tiêu cực** về thương hiệu đó từ bài viết gốc và các bình luận.
            * **Tổng hợp đánh giá chi tiết về thương hiệu**: Dựa trên các từ/cụm từ tích cực và tiêu cực, đưa ra đánh giá chi tiết về ưu và nhược điểm của từng thương hiệu.
        4.  **So sánh và đánh giá tổng quan**:
            * Xác định **thương hiệu được đánh giá tốt nhất** dựa trên số lượng và mức độ các phản hồi tích cực.
            * Xác định **thương hiệu bị đánh giá kém nhất** dựa trên số lượng và mức độ các phản hồi tiêu cực (nếu có).
            * **Phân tích so sánh chi tiết** giữa các thương hiệu, nêu rõ ưu và nhược điểm của từng thương hiệu so với các đối thủ.

        ### **Định dạng đầu ra (JSON):**

        ```json
        {{
            "brands": [
                {{
                    "name": "Tên thương hiệu",
                    "positive_feedback": ["Từ/cụm từ thể hiện sự tích cực", "Từ/cụm từ khác thể hiện sự tích cực"],
                    "negative_feedback": ["Từ/cụm từ thể hiện sự tiêu cực", "Từ/cụm từ khác thể hiện sự tiêu cực"],
                    "general_assessment": "Đánh giá chi tiết về ưu và nhược điểm của thương hiệu dựa trên các phản hồi."
                }}
            ],
            "comparison": {{
                "best_rated": "Tên thương hiệu được đánh giá tốt nhất",
                "worst_rated": "Tên thương hiệu được đánh giá kém nhất (nếu có)",
                "comparative_analysis": "Phân tích so sánh chi tiết giữa các thương hiệu."
            }}
        }}
        """
