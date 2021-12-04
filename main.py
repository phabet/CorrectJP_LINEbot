import re
import os
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

def trans_word(inputtext):
    replacements = {
'多':'乡',
'鳥':'乌',
'雨':'丽',
'両':'两',
'並':'业',
'メルカリ':'淘宝網',
'AQUOS':'HUAWEI',
'aquos':'HUAWEI',
'Aquos':'HUAWEI',
'huaweimk':'ファーウェイウェイ',
'あなた':'貴様',
'貴':'贵',
'し':'レ',
'ぶ':'ふ',
'で':'て',
'応':'应',
'ス':'ヌ',
'雑':'杂',
'貨':'货',
'見':'见',
'潰':'溃',
'め':'ぬ',
'キ':'ギ',
'ぞ':'そ',
'舐':'舐',
'絶':'绝',
'対':'对',
'得':'慧',
'溜':'贮',
'達':'们',
'jp':'cn',
'NHK':'CCTV',
'XPERIA':'HUAWEI',
'円':'人民元',
'LINEpay':'alipay',
'PayPay':'WechatPay',
'Twitter':'weibo',
'ツイッター':'ウェイボ',
'instagram':'Tiktok',
'インスタ':'Tiktok',
'ライン':'wechat',
'LINE':'wechat',
'line':'wechat',
'風':'风',
'なさい':'(しなさい)',
'強':'强',
'東京':'北京',
'シリコンバレー':'深圳',
'google':'百度',
'グーグル':'百度',
'Google':'百度',
'スカイツリー':'上海中心',
'SKY TREE':'shanghai tower',
'TOKYO':'上海',
'ハ':'八゜',
'amazon':'亚马逊',
'アマゾン':'亚马逊',
'乘':'乘',
'黑':'黑',
'snapdragon':'Kirin',
'SD':'NM',
'PUBG':'荒野行動',
'労働':'極度勞動',
'東':'东',
'ラーメン':'うーメソ',
'🇯🇵':'🇨🇳',
'🇰🇷':'🇨🇳',
'🇺🇸':'🇨🇳',
'🇬🇧':'🇨🇳',
'🇷🇺':'🇨🇳',
'🇩🇪':'🇨🇳',
'🇮🇳':'🇨🇳',
'🇿🇦':'🇨🇳',
'🇧🇷':'🇨🇳',
'オ':'才',
'愛':'爱',
'語':'语',
'ぬ':'ゐ',
'る':'ゑ',
'iphone':'HUAWEI',
'アイフォン':'ファーウェイ',
'だ':'た',
'変':'變',
'榮':'荣',
'強':'强',
'う':'ラ',
'ハ':'八',
'応':'应',
'偉':'伟',
'義':'义',
'結':'结',
'協':'协',
'調':'调',
'剤':'剂',
'様':'樣',
'セ':'乜',
'動':'动',
'評':'评',
'ファーウェイ':'华为技术有限公司',
'HUAWEI':'华为技术有限公司'}
    if inputtext:
        return re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))), lambda m: replacements[m.group()], inputtext)
    else:
        return ""
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=trans_word(event.message.text)))



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)