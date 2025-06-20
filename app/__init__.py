#Backend/app/__init__.py
from flask import Flask
from flask_cors import CORS

from app.models.token_blocklist import TokenBlocklist

from .config import Config
from .extensions import db, jwt, mail, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None
        
    from app.routes.auth_routes import auth_bp
    from app.routes.opportunity_routes import opportunity_bp
    from app.routes.dropdown_routes import dropdown_bp
    from app.routes.tag_routes import tag_bp
    from app.routes.skill_routes import skill_bp
    from app.routes.user_skills_routes import user_skills_bp
    from app.routes.user_profile_routes import profile_bp
    from .routes.post_routes import post_bp
    from .routes.follow_routes import follow_bp
    from .routes.industry_routes import industry_bp
    from .routes.public_organization_routes import public_org_bp
    from .routes.organization_routes import organization_bp
    from .routes.recommendation_routes import recommendation_bp
    from app.routes.user_participation_routes import user_participation_bp
    from app.routes.attendance_routes import attendance_bp
    from app.routes.organization_participant_routes import op_participant_bp
    from app.routes.evaluation_routes import evaluation_bp
    from app.routes.certificates_routes import certificate_bp
    from app.routes.invite_routes import invite_recommendation_bp
    from app.routes.notification_route import notification_bp
    from app.routes.notification_route import user_bp
    from app.routes.user_routes import user_routes
    from app.routes.chat_routes import chat_bp
    from app.routes.ADMIN.admin_account_routes import admin_account_bp
    from app.routes.ADMIN.user_org_admin_routes import admin_user_bp, admin_org_bp, admin_admin_bp
    from app.routes.ADMIN.admin_skills_industry_routes import skills_admin_bp, industry_admin_bp
    from app.routes.ADMIN.admin_opportunity_stats_routes import opportunity_stats_bp
    from app.routes.ADMIN.discount_codes_routes import discount_codes_bp
    from app.routes.ADMIN.ads_routes import ads_bp
    from app.routes.volunteer import volunteer_bp


    app.register_blueprint(auth_bp, url_prefix="/auth")   
    app.register_blueprint(opportunity_bp, url_prefix="/opportunities") 
    app.register_blueprint(dropdown_bp, url_prefix="/dropdown")
    app.register_blueprint(skill_bp, url_prefix="/skills")
    app.register_blueprint(tag_bp, url_prefix="/tags")
    app.register_blueprint(user_skills_bp, url_prefix="/user-skills")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(post_bp, url_prefix="/posts")
    app.register_blueprint(follow_bp, url_prefix="/follow")
    app.register_blueprint(industry_bp, url_prefix="/industries")
    app.register_blueprint(public_org_bp, url_prefix="/public/organizations")
    app.register_blueprint(organization_bp, url_prefix="/organization")
    app.register_blueprint(recommendation_bp, url_prefix="/recommendations")
    app.register_blueprint(user_participation_bp, url_prefix="/user-participation")
    app.register_blueprint(attendance_bp, url_prefix="/attendance")
    app.register_blueprint(op_participant_bp, url_prefix="/org/opportunities")
    app.register_blueprint(evaluation_bp, url_prefix="/evaluation")
    app.register_blueprint(certificate_bp, url_prefix="/certificates")
    app.register_blueprint(invite_recommendation_bp, url_prefix="/invite")
    app.register_blueprint(notification_bp, url_prefix="/notifications")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(user_routes, url_prefix="/user-routes")
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(admin_account_bp, url_prefix="/admin/accounts")
    app.register_blueprint(admin_user_bp, url_prefix="/admin/users")
    app.register_blueprint(admin_org_bp, url_prefix="/admin/organizations")
    app.register_blueprint(admin_admin_bp, url_prefix="/admin/admins")
    app.register_blueprint(skills_admin_bp, url_prefix="/admin/skills")
    app.register_blueprint(industry_admin_bp, url_prefix="/admin/industries")
    app.register_blueprint(opportunity_stats_bp, url_prefix="/admin/opportunities/stats")
    app.register_blueprint(discount_codes_bp,  url_prefix="/admin/discount-codes")
    app.register_blueprint(ads_bp, url_prefix="/admin/firebase-ads")
    app.register_blueprint(volunteer_bp, url_prefix="/volunteers")
    
    return app
