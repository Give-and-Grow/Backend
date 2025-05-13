# Backend/app/services/Dashboard/admin_account_service.py
from app.models.account import Account, Role
from app.extensions import db
from flask import jsonify
from sqlalchemy import or_
from datetime import datetime, timedelta

class AccountService:
    
    @staticmethod
    def get_all():
        return Account.query.all()

    @staticmethod
    def get_by_id(account_id):
        return Account.query.get_or_404(account_id)

    @staticmethod
    def update_role(account_id, new_role):
        account = Account.query.get_or_404(account_id)
        account.role = Role(new_role)
        db.session.commit()
        return account

    @staticmethod
    def delete(account_id):
        account = Account.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        return {"message": "Account deleted."}

    from datetime import datetime, timedelta

    @staticmethod
    def stats():
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        return {
            "total": Account.query.count(),
            "users": Account.query.filter_by(role=Role.USER).count(),
            "admins": Account.query.filter_by(role=Role.ADMIN).count(),
            "organizations": Account.query.filter_by(role=Role.ORGANIZATION).count(),
            "verified_emails": Account.query.filter_by(is_email_verified=True).count(),
            "unverified_emails": Account.query.filter_by(is_email_verified=False).count(),
            "logged_in_users": Account.query.filter(Account.last_login.isnot(None)).count(),
            "new_accounts_last_30_days": Account.query.filter(Account.created_at >= thirty_days_ago).count(),
        }


    @staticmethod
    def search(query):
        return Account.query.filter(
            or_(
                Account.username.ilike(f"%{query}%"),
                Account.email.ilike(f"%{query}%")
            )
        ).all()
