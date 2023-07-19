
from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from datetime import date,timedelta
from urllib.parse import quote
from googletrans import Translator
until=date.today()
since= until-timedelta(days=1)
# nhập từ khóa muốn tìm kiếm trên twitter
keyword = input("keyword = ")

# chọn browser là Chrome
# Khởi tạo trình duyệt Chrome với tùy chọn
# chọn browser là Chrome
# Khởi tạo trình duyệt Chrome với tùy chọn
def web_driver():
    driver = webdriver.Chrome()
    return driver

browser = web_driver()
browser.get("https://twitter.com/login")

# Điền thông tin tài khoản và mật khẩu vào các trường đăng nhập
time.sleep(5)
# Chờ trang tải hoàn tất
browser.implicitly_wait(10)
browser.find_element(By.XPATH, "//input").send_keys("rtar1003@gmail.com")
next = browser.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div")
next.click()
time.sleep(3)
browser.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input").send_keys("duclam123")
login = browser.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div")
login.click()
time.sleep(15)
f=open("C:/Users/TranDucLam/Downloads/Data/DataCrawl.csv",mode='w',encoding='utf-8')
f.close()
len_file = 0
tran=Translator()
# vòng lặp lưu data vào file
with open("C:/Users/TranDucLam/Downloads/Data/DataCrawl.csv",mode='a',encoding = 'utf-8') as out:
    writer=csv.writer(out,delimiter=',',lineterminator='\n')
    writer.writerow(['No','Context'])
    # lấy khoảng 50.000 tweet
    while(len_file<100):
        time.sleep(5)
        url = "https://twitter.com/search?q={}%20until%3A{}%20since%3A{}&src=typed_query&f=live".format(quote(keyword), until, since)
        browser.get(url)
        sleep(5)
        htmlElem = browser.find_element(by=By.TAG_NAME, value='html')
        # tạo list chứa 20 tweets ngay trước để so sánh, tránh lặp 
        contented = [] 
        len_day = 0
        # vòng lặp lấy dữ liệu theo mỗi 2 ngày, mỗi lần lấy khoảng 500 data
        while(len_day<10):
            try:
                # tìm tweets trong trang hiện tại
                local_contents = browser.find_elements(by=By.CSS_SELECTOR,value='[data-testid="tweetText"]')
                # so sánh với data trước đó để tránh lặp dữ liệu
                local_contents = [i.text for i in local_contents if i.text not in contented] 
                print(local_contents)
            except:
                browser.implicitly_wait(3)
                continue
            # Cập nhật list các tweet trước
            if len(contented) > 20:
                del contented[0:len(local_contents)]
            contented.extend(local_contents)

            for i in local_contents:
                len_file += 1
                len_day += 1
                # Dịch các tweet không phải tiếng Anh
                try:
                    translation = tran.translate(str(i)).text
                except Exception as e:
                    print("Lỗi khi dịch: ", e)
                    translation = "Lỗi khi dịch"
                
                writer.writerow([len_file, translation])
                print(len_file)
            # lệnh cuộn trang web xuống
            htmlElem.send_keys(Keys.PAGE_DOWN)
            htmlElem.send_keys(Keys.PAGE_DOWN)
            htmlElem.send_keys(Keys.PAGE_DOWN)
        #cập nhật 1 ngày trước đó
        until = until - timedelta(days=1)
        since = since - timedelta(days=1) 