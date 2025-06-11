from flask import Blueprint, request, jsonify
from app.services.ADMIN.ads_service import (
    create_ad, get_all_ads, get_ad_by_id, update_ad, delete_ad
)
from app.utils.decorators import admin_required, organization_required

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
