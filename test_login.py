# from seleniumwire import webdriver
# from selenium.webdriver.chrome.options import Options
# from time import sleep
# from crawl_data.utils.login import FacebookLogin  # Đường dẫn đúng
# from app.ai_config import settings
# import os

# # Proxy có username và password
# proxy_with_auth = "http://8c5906b99fbd1c0bcd0f916d545c565a3e7972fd941adc4317aa006946a891f861a25f4430dc443c0c40d32fb1bafe74e10e235f4324d89365209b26cb29f390:d6923sb5x8g9@proxy.toolip.io:31113"

# # Cấu hình proxy cho selenium-wire
# seleniumwire_options = {
#     'proxy': {
#         'http': proxy_with_auth,
#         'https': proxy_with_auth,
#         'no_proxy': 'localhost,127.0.0.1'
#     }
# }

# def test_facebook_login():
#     # Cấu hình Chrome
#     chrome_options = Options()
#     chrome_options.add_experimental_option("detach", True)
#     chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36")
#     chrome_options.add_argument("--disable-notifications")
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option("useAutomationExtension", False)
#     chrome_options.add_argument("--disable-cache")
#     chrome_options.add_argument("--enable-unsafe-swiftshader")
#     chrome_options.add_argument("--disable-gpu")


#     # Khởi tạo WebDriver với proxy
#     driver = webdriver.Chrome(
#         options=chrome_options,
#         seleniumwire_options=seleniumwire_options
#     )

#     # Đường dẫn file cookie
#     cookie_path = "crawl_data/data/cookies/my_cookies.pkl"
#     fb_login = FacebookLogin(driver, cookie_path)

#     # Mở Facebook
#     driver.get("https://www.facebook.com/login/?next&ref=dbl&fl&refid=8&__mmr=1&_rdr")

#     if fb_login.login_with_cookies():
#         print("✅ Login test passed!")
#     else:
#         print("❌ Login test failed!")

#     sleep(1000)

#     driver.quit()

# if __name__ == "__main__":
#     test_facebook_login()


# longanh0997@gmail.com 
# anhlong97

# thuytran19992703
# tranthuy99

# hoangtea2110421@gmail.com 
# lehoangtri1

# 61575652888003
# Brownkkyelxmcaqtq27

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from crawl_data.utils.login import FacebookLogin  # Đường dẫn đúng đến file FacebookLogin
from app.ai_config import settings
import os
from time import sleep

def test_facebook_login():
    # Cấu hình Chrome
    chrome_options = Options()

    # Keep browser open after script execution
    chrome_options.add_experimental_option("detach", True)

    # Set user agent to mimic a real browser
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36")

    # Disable automation detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Performance and stability options
    chrome_options.add_argument("--no-sandbox")  # Required for some Linux environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues in Docker
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (useful for headless or Windows)
    chrome_options.add_argument("--disable-cache")  # Prevent caching issues
    chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode

    # Disable unnecessary browser features
    chrome_options.add_argument("--disable-notifications")  # Prevent notification popups
    chrome_options.add_argument("--no-default-browser-check")  # Skip default browser check
    chrome_options.add_argument("--disable-translate")  # Disable translation prompts
    chrome_options.add_argument("--disable-infobars")  # Disable info bars

    # Security-related options (use cautiously)
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    chrome_options.add_argument("--allow-running-insecure-content")  # Allow insecure content
    chrome_options.add_argument("--disable-web-security")  # Disable web security (risky, use only if necessary)

    # Logging for debugging
    chrome_options.add_argument("--verbose")

    # Conditional GPU disable for Windows
    if os.name == 'nt':
        chrome_options.add_argument("--disable-gpu")

    # Khởi tạo WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Đường dẫn file cookie (tạo thư mục nếu chưa có)
    cookie_path = "crawl_data/data/cookies/my_cookies.pkl"           
    # Khởi tạo class login
    fb_login = FacebookLogin(driver, cookie_path)

    # Mở trang Facebook
    driver.get("https://www.facebook.com/")

    # Thử login bằng cookie hoặc tài khoản
    if fb_login.login_with_cookies():
        print("✅ Login test passed!")
    else:
        print("❌ Login test failed!")

    # Đóng trình duyệt
    driver.quit()

if __name__ == "__main__":
    test_facebook_login()

# longanh0997@gmail.com 
# anhlong97

# thuytran19992703
# tranthuy99

# hoangtea2110421@gmail.com 
# lehoangtri1

# 61575652888003
# Brownkkyelxmcaqtq27