from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import dotenv

app = FastAPI()

dotenv.load_dotenv()

line_bot_api = LineBotApi(os.getenv("LINEBOT_CHANNEL_ACCESS_TOKEN"))
line = WebhookHandler(os.getenv('LINEBOT_CHANNEL_SECRET'))

@app.post("/callback")
async def webhook(request: Request):
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')

    # get request body as text
    body_bytes = await request.body()
    body = body_bytes.decode('utf-8')

    # handle webhook body
    try:
        line.handle(body, signature)
    except InvalidSignatureError:
        return HTTPException(status_code=400, detail="Invalid signature")

    return 'OK'

@line.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )