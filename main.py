from app import create_app
from app.utils.logger import logger
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('NODE_ENV', 'development') == 'development'
    
    logger.info(f"啟動 LINE Bot 伺服器，端口: {port}")
    logger.info(f"環境模式: {os.environ.get('NODE_ENV', 'development')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)