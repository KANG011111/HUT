import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
    GOOGLE_SERVICE_ACCOUNT_EMAIL = os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL')
    GOOGLE_PRIVATE_KEY = os.getenv('GOOGLE_PRIVATE_KEY')
    PORT = int(os.getenv('PORT', 5000))
    NODE_ENV = os.getenv('NODE_ENV', 'development')
    
    @staticmethod
    def validate():
        # 必須的 LINE Bot 環境變數
        required_vars = [
            'LINE_CHANNEL_ACCESS_TOKEN',
            'LINE_CHANNEL_SECRET'
        ]
        
        # 可選的 Google Sheets 環境變數
        optional_google_vars = [
            'GOOGLE_SHEET_ID',
            'GOOGLE_SERVICE_ACCOUNT_EMAIL',
            'GOOGLE_PRIVATE_KEY'
        ]
        
        # 除錯：輸出所有環境變數的存在狀態
        print("=== 環境變數除錯資訊 ===")
        for var in required_vars + optional_google_vars:
            value = os.getenv(var)
            if value:
                print(f"{var}: 已設定 (長度: {len(value)})")
            else:
                print(f"{var}: 未設定或為空")
        
        # 檢查所有環境變數
        all_env_vars = dict(os.environ)
        line_vars = {k: v for k, v in all_env_vars.items() if 'LINE' in k.upper()}
        google_vars = {k: v for k, v in all_env_vars.items() if 'GOOGLE' in k.upper()}
        
        print(f"包含 LINE 的環境變數: {list(line_vars.keys())}")
        print(f"包含 GOOGLE 的環境變數: {list(google_vars.keys())}")
        print("========================")
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # 檢查 Google Sheets 配置
        google_vars_present = [var for var in optional_google_vars if os.getenv(var)]
        if google_vars_present and len(google_vars_present) != len(optional_google_vars):
            missing_google_vars = [var for var in optional_google_vars if not os.getenv(var)]
            print(f"警告：Google Sheets 配置不完整，缺少: {', '.join(missing_google_vars)}")
            print("將停用 Google Sheets 功能")
        
        return True