from flask import request, jsonify
from app.models.account import Account, Role
from app.extensions import db
from sqlalchemy import or_

def get_all_accounts_service(req):
    query = Account.query

    # Filters
    role = req.args.get("role")
    is_active = req.args.get("is_active")
    search = req.args.get("search")

    if role:
        query = query.filter(Account.role == Role(role))
    if is_active:
        query = query.filter(Account.is_active == (is_active.lower() == "true"))
    if search:
        query = query.filter(or_(
            Account.email.ilike(f"%{search}%"),
            Account.username.ilike(f"%{search}%")
        ))

    # Pagination
    page = int(req.args.get("page", 1))
    per_page = int(req.args.get("per_page", 10))
    pagination = query.order_by(Account.created_at.desc()).paginate(page=page, per_page=per_page)

    accounts = [
        {
            "id": acc.id,
            "email": acc.email,
            "username": acc.username,
            "role": acc.role.value,
            "is_active": acc.is_active,
            "is_email_verified": acc.is_email_verified,
            "created_at": acc.created_at,
        } for acc in pagination.items
    ]

    return jsonify({
        "accounts": accounts,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })

def get_account_service(account_id):
    account = Account.query.get_or_404(account_id)
    return jsonify({
        "id": account.id,
        "email": account.email,
        "username": account.username,
        "role": account.role.value,
        "is_active": account.is_active,
        "is_email_verified": account.is_email_verified,
        "last_login": account.last_login,
        "created_at": account.created_at,
    })


def get_account_stats_service():
    total = Account.query.count()
    active = Account.query.filter_by(is_active=True).count()
    inactive = Account.query.filter_by(is_active=False).count()
    admins = Account.query.filter_by(role=Role.ADMIN).count()
    users = Account.query.filter_by(role=Role.USER).count()
    orgs = Account.query.filter_by(role=Role.ORGANIZATION).count()

    return jsonify({
        "total": total,
        "active": active,
        "inactive": inactive,
        "admins": admins,
        "users": users,
        "organizations": orgs
    })
