from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from app.config import Config
from app.services.line_service import LineService
from app.utils.logger import logger

line_bp = Blueprint('line', __name__)

# 延遲初始化，避免在導入時初始化
line_bot_api = None
handler = None
line_service = None

@line_bp.route('/line/test', methods=['GET'])
def test_endpoint():
    return {
        'status': 'success',
        'message': 'LINE Bot API is working',
        'endpoint': '/api/line/webhook'
    }

def _init_line_services():
    """初始化 LINE 服務"""
    global line_bot_api, handler, line_service
    
    if line_bot_api is None:
        # 驗證環境變數
        if not Config.LINE_CHANNEL_ACCESS_TOKEN:
            logger.error("LINE_CHANNEL_ACCESS_TOKEN 環境變數未設定")
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN 環境變數未設定")
        
        if not Config.LINE_CHANNEL_SECRET:
            logger.error("LINE_CHANNEL_SECRET 環境變數未設定")
            raise ValueError("LINE_CHANNEL_SECRET 環境變數未設定")
        
        line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        line_service = LineService()
        
        # 註冊事件處理器
        _register_handlers()
        
        logger.info("LINE 服務初始化成功")

@line_bp.route('/line/webhook', methods=['GET', 'POST'])
def webhook():
    # 處理 GET 請求（用於驗證）
    if request.method == 'GET':
        return 'LINE Bot webhook endpoint is working!', 200
    
    # 處理 POST 請求（實際的 webhook）
    try:
        # 初始化 LINE 服務
        _init_line_services()
        
        signature = request.headers.get('X-Line-Signature')
        if not signature:
            logger.error("缺少 X-Line-Signature 標頭")
            abort(400)
        
        body = request.get_data(as_text=True)
        
        logger.info(f"收到 LINE webhook 請求: {body}")
        
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("無效的簽章")
        abort(400)
    except Exception as e:
        logger.error(f"處理 webhook 時發生錯誤: {str(e)}")
        abort(500)
    
    return 'OK'

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

# 註冊事件處理器（延遲註冊）
def _register_handlers():
    """註冊事件處理器"""
    if handler is not None:
        handler.add(MessageEvent, message=TextMessage)(handle_text_message)