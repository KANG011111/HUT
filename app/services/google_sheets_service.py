import gspread
from google.oauth2.service_account import Credentials
from app.config import Config
from app.utils.logger import logger

class GoogleSheetsService:
    def __init__(self):
        self.sheet = None
        self._init_google_sheets()
    
    def _init_google_sheets(self):
        """初始化 Google Sheets 連線"""
        try:
            # 檢查必要的環境變數
            if not Config.GOOGLE_SERVICE_ACCOUNT_EMAIL:
                logger.error("GOOGLE_SERVICE_ACCOUNT_EMAIL 環境變數未設定")
                raise ValueError("GOOGLE_SERVICE_ACCOUNT_EMAIL 環境變數未設定")
            
            if not Config.GOOGLE_PRIVATE_KEY:
                logger.error("GOOGLE_PRIVATE_KEY 環境變數未設定")
                raise ValueError("GOOGLE_PRIVATE_KEY 環境變數未設定")
            
            # 設定 Google Sheets 權限範圍
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            
            # 建立憑證
            credentials_info = {
                "type": "service_account",
                "project_id": "linebot-466112",
                "private_key_id": "a416f5022444968cc0a357c9d2bdb089644974b5",
                "private_key": Config.GOOGLE_PRIVATE_KEY.replace('\\n', '\n'),
                "client_email": Config.GOOGLE_SERVICE_ACCOUNT_EMAIL,
                "client_id": "109585485390930364250",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{Config.GOOGLE_SERVICE_ACCOUNT_EMAIL}",
                "universe_domain": "googleapis.com"
            }
            
            credentials = Credentials.from_service_account_info(credentials_info, scopes=scope)
            gc = gspread.authorize(credentials)
            
            # 開啟 Google Sheets
            self.sheet = gc.open_by_key(Config.GOOGLE_SHEET_ID).sheet1
            
            # 確保標題列存在
            self._ensure_headers()
            
            logger.info("Google Sheets 連線初始化成功")
            
        except Exception as e:
            logger.error(f"Google Sheets 初始化失敗: {str(e)}")
            logger.error(f"Google Service Account Email: {Config.GOOGLE_SERVICE_ACCOUNT_EMAIL}")
            logger.error(f"Google Sheet ID: {Config.GOOGLE_SHEET_ID}")
            raise
    
    def _ensure_headers(self):
        """確保工作表有正確的標題列"""
        try:
            headers = ['時間', '用戶ID', '用戶名稱', '訊息內容', '訊息類型']
            
            # 檢查第一行是否為標題列
            first_row = self.sheet.row_values(1)
            if not first_row or first_row != headers:
                self.sheet.insert_row(headers, 1)
                logger.info("已插入標題列")
                
        except Exception as e:
            logger.error(f"設定標題列時發生錯誤: {str(e)}")
            raise
    
    def save_message(self, timestamp, user_id, user_name, message_content, message_type):
        """儲存訊息到 Google Sheets"""
        try:
            row_data = [timestamp, user_id, user_name, message_content, message_type]
            self.sheet.append_row(row_data)
            
            logger.info(f"成功儲存訊息到 Google Sheets: {message_content}")
            
        except Exception as e:
            logger.error(f"儲存訊息到 Google Sheets 時發生錯誤: {str(e)}")
            # 重試連線
            self._init_google_sheets()
            try:
                self.sheet.append_row(row_data)
                logger.info("重試後成功儲存訊息")
            except Exception as retry_error:
                logger.error(f"重試後仍無法儲存訊息: {str(retry_error)}")
                raise
    
    def get_all_messages(self):
        """獲取所有訊息"""
        try:
            all_records = self.sheet.get_all_records()
            return all_records
        except Exception as e:
            logger.error(f"獲取所有訊息時發生錯誤: {str(e)}")
            raise
    
    def get_message_count(self):
        """獲取訊息總數"""
        try:
            all_values = self.sheet.get_all_values()
            # 扣除標題列
            return len(all_values) - 1 if all_values else 0
        except Exception as e:
            logger.error(f"獲取訊息數量時發生錯誤: {str(e)}")
            raise