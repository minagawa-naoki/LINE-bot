# configの場所を変えているからできない
#tweetを投稿
import config
import tweepy
import schedule

#-------------Twitter
def twitter(word):
    submission_word = word  # リスト作成
    
    consumer_key = config.CONSUMER_KEY
    consumer_secret = config.CONSUMER_SECRET
    access_token = config.ACCESS_TOKEN
    access_token_secret = config.ACCESS_TOKEN_SECRET
    
    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # ツイートを投稿
    api.update_status(submission_word)


#---------------授業出席
from selenium import webdriver
import time
import os
import signal
import config

def attend(url):
    driver = webdriver.Chrome(executable_path=r"C:\Users\g020c1107\Desktop\VScode_folder\python_folder\.vscode\制作物\自動出席\chromedriver.exe")
    driver.get(url)

    time.sleep(2)  # 10秒
    elem_login_btn = driver.find_element_by_xpath("//div/div[2]/div/div/div/div/div/div[2]/div[3]/div/a")
    elem_login_btn.click()
    time.sleep(2)  # 5秒
    elem_username = driver.find_element_by_id("identifierId")  # 場所を取得
    elem_username.send_keys(config.neec_user_name)  # 入力
    elem_login_btn = driver.find_element_by_xpath("//div/button/div[2]")
    elem_login_btn.click()  # クリック
    time.sleep(2)  # 5秒
    elem_password = driver.find_element_by_name("password")  # 場所を取得
    elem_password.send_keys(config.neec_pass)  # 入力
    elem_login_btn = driver.find_element_by_xpath("//div/button/div[2]")
    elem_login_btn.click()  # クリック
    time.sleep(5)  # 5秒driver.find_element_by_class_name('multiline') content = driver.find_element_by_css_selector('p.content') //*[@id="course-info-container-457-4"]/div/div/a/span[3]
    elem_login_btn = driver.find_element_by_xpath("//div/div/div[2]/div[1]/a/img")
    elem_login_btn.click()  # クリック //*[@id="next-activity-link"]
    elem_login_btn = driver.find_element_by_id("next-activity-link")
    elem_login_btn.click()
    time.sleep(10)  # 5秒
    driver.close()
    return "出席完了しました。"

#-------------特売情報
def tokubai(number):
    print(number)
    global error_name
    global try_number_1
    global try_number_2
    if len(number[:]) != 8:
        error_name = "郵便番号の入力に失敗しています。\n(例:111-2222"
        return error_name
    else:
        try:
            try_number_1 = int(number[0:3])
            try_number_2 = int(number[4:9])
        except ValueError:
            error_name = "郵便番号の入力に失敗しています。\n(例:111-2222"
            return error_name
        else:
            driver = webdriver.Chrome(executable_path=r"")
            driver.get("https://tokubai.co.jp/")
            driver.implicitly_wait(10)
            driver.find_element_by_name("first_digits").send_keys(number[0:3])  # 一つ目の郵便番号 入力
            time.sleep(2)
            driver.find_element_by_name("second_digits").send_keys(number[4:9])  # 二つ目の郵便番号 入力  
            driver.find_elements_by_name("commit")[1].click()  # 検索 クリック
            driver.implicitly_wait(20)
            web_url = driver.current_url
            time.sleep(5)
            driver.close()
            return web_url

def num(num):
    if num == 100:
        num_1 = num*2
        return num_1
    else:
        num_2 = num*3
        return num_2




"""------------------授業名とmoodleURL-----------"""


lesson = {"授業名１":"授業名１URL",
"授業名２":"授業名２URL"
}
