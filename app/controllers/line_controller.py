from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from app.config import Config
from app.services.line_service import LineService
from app.utils.logger import logger

line_bp = Blueprint('line', __name__)

line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
line_service = LineService()

@line_bp.route('/line/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    logger.info(f"收到 LINE webhook 請求: {body}")
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("無效的簽章")
        abort(400)
    except Exception as e:
        logger.error(f"處理 webhook 時發生錯誤: {str(e)}")
        abort(500)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    try:
        user_id = event.source.user_id
        message_text = event.message.text
        timestamp = event.timestamp
        
        logger.info(f"收到用戶 {user_id} 的訊息: {message_text}")
        
        # 處理訊息並儲存到 Google Sheets
        line_service.process_message(user_id, message_text, timestamp)
        
        # 回覆確認訊息
        reply_message = f"已收到您的訊息：{message_text}"
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=reply_message)
        )
        
    except Exception as e:
        logger.error(f"處理文字訊息時發生錯誤: {str(e)}")
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="抱歉，處理您的訊息時發生錯誤，請稍後再試。")
        )