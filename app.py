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

app = Flask(__name__)

line_bot_api = LineBotApi('njcOYYtKjWJvEwUY3YBF+ZtRyBxYNI0JjamaDVdwsena4LjWhoWIBzDEe06awNJKbd41wG0UO+SBozhc/7uEqr7M5ZQ97q+HpwFaIuCwrEmOIwZ9/oh5MenNUaRzi2klnpOXdWFz+t95lqHXya5msgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c281b9d8d694aef8c3faf32af61be473')


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
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
