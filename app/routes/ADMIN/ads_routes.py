from flask import Blueprint, request, jsonify
from datetime import datetime
from uuid import uuid4
from app.services.ADMIN.ads_service import (
    create_ad, get_all_ads, get_ad_by_id,
    update_ad, delete_ad,
    submit_ad_request_service, get_pending_ads_service,
    approve_ad_service, reject_ad_service
)
from app.utils.decorators import admin_required
from app.utils.email import send_ad_status_email

ads_bp = Blueprint("firebase_ads", __name__)

@ads_bp.route("/create", methods=["POST"])
@admin_required
def create_ad_route():
    data = request.get_json()
    ad_id = create_ad(data)
    return jsonify({"message": "Ad created", "id": ad_id}), 201

@ads_bp.get("/")
def get_ads_route():
    return jsonify(get_all_ads()), 200

@ads_bp.get("/<string:ad_id>")
def get_ad_route(ad_id):
    ad = get_ad_by_id(ad_id)
    if not ad:
        return jsonify({"message": "Ad not found"}), 404
    return jsonify(ad)

@ads_bp.put("/<string:ad_id>")
@admin_required
def update_ad_route(ad_id):
    data = request.get_json()
    success = update_ad(ad_id, data)
    if not success:
        return jsonify({"message": "Ad not found"}), 404
    return jsonify({"message": "Ad updated"})

@ads_bp.delete("/<string:ad_id>")
@admin_required
def delete_ad_route(ad_id):
    success = delete_ad(ad_id)
    if not success:
        return jsonify({"message": "Ad not found"}), 404
    return jsonify({"message": "Ad deleted"})

@ads_bp.route("/request", methods=["POST"])
def submit_ad_request():
    data = request.get_json()
    ad_id = submit_ad_request_service(data)
    return jsonify({"message": "Ad request submitted", "id": ad_id}), 201

@ads_bp.get("/requests")
@admin_required
def get_pending_ads():
    return jsonify(get_pending_ads_service()), 200

@ads_bp.put("/requests/<string:ad_id>/approve")
@admin_required
def approve_ad(ad_id):
    result = approve_ad_service(ad_id)
    if not result:
        return jsonify({"message": "Ad request not found"}), 404
    return jsonify({"message": "Ad approved, published, and email sent"})

@ads_bp.put("/requests/<string:ad_id>/reject")
@admin_required
def reject_ad(ad_id):
    data = request.get_json()
    result = reject_ad_service(ad_id, data.get("response_message", "No reason provided"))
    if not result:
        return jsonify({"message": "Ad request not found"}), 404
    return jsonify({"message": "Ad rejected and email sent"})
