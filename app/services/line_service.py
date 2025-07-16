from datetime import datetime
from linebot import LineBotApi
from app.config import Config
from app.services.google_sheets_service import GoogleSheetsService
from app.utils.logger import logger

class LineService:
    def __init__(self):
        self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        self.sheets_service = GoogleSheetsService()
    
    def process_message(self, user_id, message_text, timestamp):
        """處理接收到的訊息"""
        try:
            # 轉換時間戳記
            formatted_time = self._format_timestamp(timestamp)
            
            # 獲取用戶資訊
            user_name = self._get_user_name(user_id)
            
            # 儲存到 Google Sheets
            self.sheets_service.save_message(
                timestamp=formatted_time,
                user_id=user_id,
                user_name=user_name,
                message_content=message_text,
                message_type='text'
            )
            
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
            profile = self.line_bot_api.get_profile(user_id)
            return profile.display_name
        except Exception as e:
            logger.error(f"獲取用戶名稱時發生錯誤: {str(e)}")
            return "未知用戶"