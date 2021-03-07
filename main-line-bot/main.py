from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import time
from selenium import webdriver
import config
import function
import tweepy
import threading

nones = lambda n: ["" for _ in range(n)]  # グローバル変数の初期値として
change_num,word,lesson,number,web_url,url,confirmation = nones(7)  # 変数の数

app = Flask(__name__)

line_bot_api = LineBotApi(config.Channel_access_token)
handler = WebhookHandler(config.Channel_secret)


@app.route("/")  # webサイトに接続
def test():
    return "接続できました。"  # 接続確認のため

@app.route("/callback", methods=['POST'])  # /callbackをつけることでweb hookにここと接続するようにする
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)  # 返信関係　event.message.textでメッセージを取得できている 
def handle_message(event):
    global change_num,word,lesson,number,web_url,url,confirmation  # グローバル変数まとめ

#---------------実行内容をしっかりする
    if change_num == 1 and event.message.text == "はい":
        reply_massage = "特売情報を取得します。\n現在地の郵便番号を送信してください。"        
    elif change_num == 1 and event.message.text == "いいえ":
        reply_massage = "分かりました。\nやりたいことを記入してください。\n(例 特売情報が知りたい。など"
        change_num = 0
    elif change_num == 1:
        number = event.message.text
        web_url = function.tokubai(number)
        if web_url == "郵便番号の入力に失敗しています。\n(例:111-2222":
            reply_massage = "郵便番号の入力に失敗しています。\n(例:111-2222 \nもう一度しますか？\nはいorいいえ"
        else:
            reply_massage = "近くの特売情報のURLです \n"+web_url+"\n確認してみてください。"  # seleniumを使ってトクバイからURLを取得し送信している
            change_num = 0  # リセット
    elif change_num == 2:
        reply_massage = "Twitterへの投稿内容は「"+event.message.text+"」でよろしいでしょうか？ \n はいorいいえ"  # 間違えているかもしてないから最終確認として
        word = event.message.text  # 投稿する内容を変数にいれている
        change_num += 2  # 確認のため
    elif event.message.text == "はい" and change_num == 4:  # はいだった場合
        try:
            function.twitter(word)  # 投稿
        except tweepy.error.TweepError:
            reply_massage = "何らかのエラーによって投稿できませんでした。他の内容で投稿してください\n(原因:同じ内容の投稿を12時間前にしたなど…"
            change_num = 2
        else:
            reply_massage = "Twitterへ投稿しました"  # 投稿完了のメッセージを送信
            change_num = 0  # リセット
    elif event.message.text == "いいえ" and change_num == 4:  # いいえだった場合
        reply_massage = "Twitterの内容を送信してください"  # 新しく投稿内容を送信する
        change_num = 2  # 確認画面に戻る
#---------------実行したい内容を指定する
    elif "特売" in event.message.text:
        reply_massage = "特売情報を取得します。\n現在地の郵便番号を送信してください。"
        change_num = 1
    elif "Twitter" in event.message.text:
        reply_massage = "Twitterの内容を送信してください"
        change_num = 2
    else:
        reply_massage = "やりたいことを記入してください。\n(例 特売情報が知りたい。など"  # もしかしたら、いい感じにif文か抜けるかもしれないから
        change_num = 0

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_massage))  # ここでreply_massageと入れただけで返信できるよう短縮させている

if __name__ == "__main__":
    app.run()