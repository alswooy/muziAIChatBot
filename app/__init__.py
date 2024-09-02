from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 앱 설정 불러오기
    # app.config.from_pyfile('config.py')

    # 라우트 등록
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app