import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_confirm_review(to_email: str, brand_name: str, dashboard_link: str):
    # Thông tin SMTP (dùng Gmail SMTP demo)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "trong219911@student.nctu.edu.vn"
    from_password = "cvpx ecew jiea ewtb"  # Lưu ý: dùng App Password nếu bật bảo mật 2 lớp

    # Tiêu đề và nội dung
    subject = f"Đánh giá thương hiệu '{brand_name}' đã hoàn tất"
    body = f"""
    <html>
    <body>
        <p>Chào bạn,</p>
        <p>Hệ thống đã hoàn tất việc đánh giá thương hiệu <strong>{brand_name}</strong>.</p>
        <p>Bạn có thể xem trực quan đánh giá tại link dưới đây:</p>
        <p><a href="{dashboard_link}" target="_blank" style="color: #7ABFEF;">Xem đánh giá tại đây</a></p>
        <br>
        <p>Trân trọng,<br>Hệ thống đánh giá thương hiệu</p>
    </body>
    </html>
    """

    try:
        # Tạo email message
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        # Kết nối SMTP và gửi
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(message)
        server.quit()

        print(f"Đã gửi email xác nhận tới {to_email}")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")