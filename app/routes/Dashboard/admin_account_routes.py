# Backend/app/routes/Dashboard/admin_account_routes.py
from flask import Blueprint, request, jsonify
from app.services.Dashboard.admin_account_service import AccountService
from app.utils.decorators import admin_required, organization_required

admin_account_bp = Blueprint("admin_account", __name__)

@admin_account_bp.get("/")
@admin_required
def list_accounts():
    accounts = AccountService.get_all()
    return jsonify([
        {
            "id": a.id,
            "email": a.email,
            "username": a.username,
            "role": a.role.value,
            "is_email_verified": a.is_email_verified,
            "created_at": a.created_at.isoformat() if a.created_at else None,
            "last_login": a.last_login.isoformat() if a.last_login else None
        }
        for a in accounts
    ]) 

@admin_account_bp.get("/<int:account_id>")
@admin_required
def get_account(account_id):
    account = AccountService.get_by_id(account_id)
    return jsonify(
        id=account.id,
        email=account.email,
        username=account.username,
        role=account.role.value,
        is_email_verified=account.is_email_verified,
        created_at=account.created_at.isoformat() if account.created_at else None,
        last_login=account.last_login.isoformat() if account.last_login else None
    )


@admin_account_bp.get("/search")
@admin_required
def search_accounts():
    q = request.args.get("q", "")
    results = AccountService.search(q)
    return jsonify([{"id": a.id, 
                    "email": a.email,
                    "username": a.username,
                    "role": a.role.value,
                    "is_email_verified": a.is_email_verified,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                    "last_login": a.last_login.isoformat() if a.last_login else None
                    } for a in results])
                    

@admin_account_bp.get("/stats")
@admin_required
def get_stats():
    return jsonify(AccountService.stats())

@admin_account_bp.delete("/<int:account_id>")
@admin_required
def delete_account(account_id):
    return jsonify(AccountService.delete(account_id))

@admin_account_bp.patch("/<int:account_id>/role")
@admin_required
def change_role(account_id):
    new_role = request.json.get("role")
    updated = AccountService.update_role(account_id, new_role)
    return jsonify({"id": updated.id, "new_role": updated.role.value})
