from utils.login import FacebookLogin
from utils.driver import Driver
import random



# Khởi tạo driver
cookies_file = "crawl_data\data\cookies\my_cookies.pkl"


driver = Driver(chrome_driver_path="crawl_data\chrome_driver\chromedriver.exe", headless=False).get_driver()
word_search = "Tôn Hoa Sen"

FacebookLogin(driver=driver, cookie_path=cookies_file).login_with_cookies()
driver.get(f"https://www.facebook.com/search/pages/?q={word_search}&locale=vi_VN")