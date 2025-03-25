from flask import Flask
from .extensions import db, jwt, mail  
from .routes.auth import auth_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    with app.app_context():
        db.create_all()
    return app