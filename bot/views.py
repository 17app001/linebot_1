from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


def index(requests):
    return HttpResponse("test!")


@csrf_exempt
def callback(request):
    words = ['早安~你好，今天好嗎?', '天氣很不錯!', '我準備去上班~', '快中午了，肚子好餓?',
             '再說一次?']
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    text = event.message.text
                    print(text)
                    # 程式練習(使用者輸入樂透=>給予六個號碼跟一個特別號)
                    if '電影' in text:
                        message = 'https://movies.yahoo.com.tw/chart.html'
                    elif '台北捷運' in text:
                        message = 'https://kuopoting.github.io/k1/'
                    elif '樂透' in text:
                        message = lotto()
                    elif '早安' in text:
                        message = '早安你好!'
                    else:
                        message = random.choice(words)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=message)
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='無法解析')
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def lotto():
    numbers = sorted(random.sample(range(1, 50), 6))
    result = ' '.join(map(str, numbers))
    n = random.randint(1, 50)

    return f'{result} 特別號:{n}'
