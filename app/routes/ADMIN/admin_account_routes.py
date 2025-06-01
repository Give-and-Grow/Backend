#Backend/app/routes/ADMIN/admin_account_routes.py
from flask import Blueprint, request, jsonify
from app.services.ADMIN.admin_account_service import (
    get_all_accounts_service,
    get_account_service,
    get_account_stats_service
)

admin_account_bp = Blueprint("admin_account_bp", __name__, url_prefix="/admin/accounts")

@admin_account_bp.route("/", methods=["GET"])
def get_all_accounts():
    return get_all_accounts_service(request)

@admin_account_bp.route("/<int:account_id>", methods=["GET"])
def get_account(account_id):
    return get_account_service(account_id)

@admin_account_bp.route("/stats", methods=["GET"])
def get_account_stats():
    return get_account_stats_service()
