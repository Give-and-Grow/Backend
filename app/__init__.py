#Backend/app/__init__.py
from flask import Flask
from flask_cors import CORS

from app.models.token_blocklist import TokenBlocklist

from .config import Config
from .extensions import db, jwt, mail, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cors = CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None

    from .routes.admin_organization import admin_org_bp
    from .routes.auth import auth_bp
    from .routes.industry_routes import industry_bp
    from .routes.organization import organization_bp
    from .routes.public_organization import public_org_bp
    from .routes.user_profile import profile_bp
    from .routes.opportunity_routes import opportunity_bp
    from .routes.skill_routes import skill_bp
    from .routes.user_skills_routes import user_skills_bp
    from .routes.dropdown import dropdown_bp
    from .routes.tag_routes import tag_bp
    from .routes.opportunity_participant_routes import opportunity_participant_bp
    from .routes.recommendation import recommendation_bp
    from .routes.Dashboard.admin_account_routes import admin_account_bp
    from .routes.follow_routes import follow_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(organization_bp, url_prefix="/organization")
    app.register_blueprint(public_org_bp, url_prefix="/public/organizations")
    app.register_blueprint(admin_org_bp, url_prefix="/admin/organizations")
    app.register_blueprint(industry_bp, url_prefix="/industries")
    app.register_blueprint(opportunity_bp, url_prefix="/opportunities")
    app.register_blueprint(skill_bp, url_prefix="/skills")
    app.register_blueprint(user_skills_bp, url_prefix="/user-skills")
    app.register_blueprint(dropdown_bp, url_prefix="/dropdown")
    app.register_blueprint(tag_bp, url_prefix="/tags")
    app.register_blueprint(opportunity_participant_bp, url_prefix="/opportunity-participants")
    app.register_blueprint(recommendation_bp, url_prefix="/recommendations")
    app.register_blueprint(admin_account_bp,  url_prefix="/admin/accounts")
    app.register_blueprint(follow_bp, url_prefix="/follow")

    
    return app
