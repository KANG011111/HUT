from datetime import datetime
from linebot import LineBotApi
from app.config import Config
from app.services.google_sheets_service import GoogleSheetsService
from app.utils.logger import logger

class LineService:
    def __init__(self):
        self.line_bot_api = None
        self.sheets_service = None
        self._init_services()
    
    def _init_services(self):
        """初始化服務"""
        if self.line_bot_api is None:
            if Config.LINE_CHANNEL_ACCESS_TOKEN:
                self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
            else:
                logger.error("LINE_CHANNEL_ACCESS_TOKEN 未設定，無法初始化 LINE Bot API")
        
        if self.sheets_service is None:
            try:
                self.sheets_service = GoogleSheetsService()
            except Exception as e:
                logger.error(f"Google Sheets 服務初始化失敗: {str(e)}")
                self.sheets_service = None
    
    def process_message(self, user_id, message_text, timestamp):
        """處理接收到的訊息"""
        try:
            # 轉換時間戳記
            formatted_time = self._format_timestamp(timestamp)
            
            # 獲取用戶資訊
            user_name = self._get_user_name(user_id)
            
            # 儲存到 Google Sheets
            if self.sheets_service:
                self.sheets_service.save_message(
                    timestamp=formatted_time,
                    user_id=user_id,
                    user_name=user_name,
                    message_content=message_text,
                    message_type='text'
                )
            else:
                logger.warning("Google Sheets 服務未初始化，無法儲存訊息")
            
            logger.info(f"成功處理用戶 {user_id} 的訊息: {message_text}")
            
        except Exception as e:
            logger.error(f"處理訊息時發生錯誤: {str(e)}")
            raise
    
    def _format_timestamp(self, timestamp):
        """格式化時間戳記"""
        try:
            # LINE 的時間戳記是毫秒，需要轉換為秒
            dt = datetime.fromtimestamp(timestamp / 1000.0)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.error(f"格式化時間戳記時發生錯誤: {str(e)}")
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _get_user_name(self, user_id):
        """獲取用戶名稱"""
        try:
            if self.line_bot_api:
                profile = self.line_bot_api.get_profile(user_id)
                return profile.display_name
            else:
                logger.warning("LINE Bot API 未初始化，無法獲取用戶名稱")
                return "未知用戶"
        except Exception as e:
            logger.error(f"獲取用戶名稱時發生錯誤: {str(e)}")
            return "未知用戶"