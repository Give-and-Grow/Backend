from flask import Flask
from .extensions import db, jwt, mail,migrate
from .routes.auth import auth_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # from models.token_blocklist import TokenBlocklist

    # @jwt.token_in_blocklist_loader
    # def check_if_token_revoked(jwt_header, jwt_payload):
    #     jti = jwt_payload['jti']
    #     token = TokenBlocklist.query.filter_by(jti=jti).first()
    #     return token is not None


    from app.models import TokenBlocklist, User
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
          

    return app