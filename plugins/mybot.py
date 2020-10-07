import json
import re

from slackbot.bot import default_reply
from slackbot.bot import respond_to


default_word = 'ちょっとわからないです。'


# デフォルトの返事
@default_reply()
def default_func(message):
    message.reply(default_word)


# help応答する
@respond_to('help', re.IGNORECASE)
def mention_help(message):

    fields = [
        {
            "title": "kubectl hogehoge",
            "value": "クラスター上で任意のkubectlコマンドが実行できます！"
        },
        {
            "title": "Pod大丈夫？",
            "value": "クラスター上のPodが正常か教えてくれます！"
        },
        {
            "title": "[namespace]の[pod_name]を削除して",
            "value": "クラスター上のPodを削除してくれます！" 
        },
        {
            "title": "ポッド表示して",
            "value": "Podの一覧を取得" 
        }
    ]

    attachments = [{
        'pretext': '以下の機能があります！',
        'fields': fields
    }]
    message.send_webapi('', json.dumps(attachments))


# こんにちはに応答する
@respond_to('hello', re.IGNORECASE)
@respond_to('こんにちは|こんにちわ')
def mention_hello(message):
    message.reply('こんにちは！')


# こんばんはに応答する
@respond_to('こんばんは|こんばんわ')
def mention_goodeveing(message):
    message.reply('こんばんは！')


# おはように応答する
@respond_to('おはよう')
def mention_goodmoring(message):
    message.reply('おはよう！')


# ありがとうに応答する
@respond_to('ありがとう')
def mention_thanks(message):
    message.reply('どういたしまして！')
