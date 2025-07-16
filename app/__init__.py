from flask import Flask
from app.config import Config
from app.controllers.line_controller import line_bp

def create_app():
    app = Flask(__name__)
    
    # WI°ƒŠx
    Config.validate()
    
    # ;ŠÍ
    app.register_blueprint(line_bp, url_prefix='/api')
    
    # e·¢åïÞ
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'LINE Bot is running'}
    
    # 9ï1
    @app.route('/', methods=['GET'])
    def index():
        return {'message': 'LINE Bot + Google Sheets API', 'version': '1.0.0'}
    
    return app