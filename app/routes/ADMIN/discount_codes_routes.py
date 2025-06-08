from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from app.utils.decorators import admin_required, organization_required

discount_codes_bp = Blueprint("discount_codes_admin", __name__)
db_firestore = firestore.client()


@discount_codes_bp.post("/")
@admin_required
def create_discount_code():
    data = request.json
    doc_ref = db_firestore.collection("discount_codes").document()
    doc_ref.set({
        "store_name": data["store_name"],
        "code": data["code"],
        "points_required": data["points_required"]
    })
    return jsonify({"message": "Discount code created", "id": doc_ref.id}), 201


@discount_codes_bp.get("/")
@admin_required
def get_all_discount_codes():
    docs = db_firestore.collection("discount_codes").stream()
    codes = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    return jsonify(codes)


@discount_codes_bp.get("/<code_id>")
@admin_required
def get_discount_code(code_id):
    doc = db_firestore.collection("discount_codes").document(code_id).get()
    if not doc.exists:
        return jsonify({"error": "Discount code not found"}), 404
    return jsonify({"id": doc.id, **doc.to_dict()})


@discount_codes_bp.put("/<code_id>")
@admin_required
def update_discount_code(code_id):
    data = request.json
    doc_ref = db_firestore.collection("discount_codes").document(code_id)
    if not doc_ref.get().exists:
        return jsonify({"error": "Discount code not found"}), 404
    doc_ref.update(data)
    return jsonify({"message": "Discount code updated"})


@discount_codes_bp.delete("/<code_id>")
@admin_required
def delete_discount_code(code_id):
    doc_ref = db_firestore.collection("discount_codes").document(code_id)
    if not doc_ref.get().exists:
        return jsonify({"error": "Discount code not found"}), 404
    doc_ref.delete()
    return jsonify({"message": "Discount code deleted"})
