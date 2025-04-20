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
    
    GENERATE_EVALUATE_PROMPT = """
        Bạn là một AI ngôn ngữ có khả năng phân tích ngữ nghĩa của văn bản.

        Nhiệm vụ của bạn là:
        - Phân tích tổng thể bình luận người dùng đã cung cấp bên dưới để xác định cảm xúc chung của bình luận: tích cực, tiêu cực, trung tính, hoặc pha trộn (vừa tích cực vừa tiêu cực).
        - Sau đó, trích xuất các từ hoặc cụm từ mang cảm xúc phù hợp, chia thành hai nhóm:
            - "tu_tot": chứa các từ hoặc cụm từ thể hiện cảm xúc tích cực.
            - "tu_xau": chứa các từ hoặc cụm từ thể hiện cảm xúc tiêu cực.

        Yêu cầu:
        - Nếu bình luận chỉ chứa emoji, ký hiệu đặc biệt (?, !, ., ...) hoặc không có từ ngữ rõ ràng → coi là bình luận trung tính → trả về hai danh sách rỗng.
        - Nếu bình luận là tích cực → chỉ trích xuất "tu_tot", để "tu_xau" rỗng.
        - Nếu bình luận là tiêu cực → chỉ trích xuất "tu_xau", để "tu_tot" rỗng.
        - Nếu bình luận vừa tích cực vừa tiêu cực → trích xuất cả "tu_tot" và "tu_xau".
        - Nếu không có từ tốt hoặc từ xấu tương ứng → vẫn trả về danh sách rỗng.
        - Chỉ trích xuất các từ hoặc cụm từ thể hiện cảm xúc rõ ràng, không suy luận hay diễn giải thêm.
        - Không đưa ra bất kỳ lời giải thích nào.
        - Không được lặp lại nội dung bình luận.
        - Không trả lời bất kỳ nội dung nào ngoài kết quả JSON.
        - Tuyệt đối không được yêu cầu thêm dữ liệu đầu vào.
        - Chỉ trả về duy nhất kết quả đúng định dạng JSON sau:

        {{
            "tu_tot": [<danh sách từ tốt>],
            "tu_xau": [<danh sách từ xấu>]
        }}

        Lưu ý:
        - Kết quả trả về chỉ chứa một cặp tu_tot và tu_xau.
        - Mỗi trường là danh sách các từ hoặc cụm từ tương ứng, không phải là đối tượng hay cấu trúc lồng nhau.
        - Luôn đảm bảo kết quả trả về là JSON hợp lệ, không có phần thừa hoặc sai cấu trúc.
    """

