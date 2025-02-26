from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Регистрируем blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Регистрируем обработчики ошибок
    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app
