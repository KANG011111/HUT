import logging
import os
from datetime import datetime

def setup_logger():
    """設定日誌記錄器"""
    
    # 建立日誌目錄
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 設定日誌格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 建立日誌記錄器
    logger = logging.getLogger('linebot')
    logger.setLevel(logging.INFO)
    
    # 避免重複添加處理器
    if not logger.handlers:
        # 控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # 檔案處理器
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(log_dir, f'linebot_{today}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # 錯誤檔案處理器
        error_log_file = os.path.join(log_dir, f'linebot_error_{today}.log')
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(log_format)
        error_handler.setFormatter(error_formatter)
        logger.addHandler(error_handler)
    
    return logger

# 建立全域日誌記錄器
logger = setup_logger()