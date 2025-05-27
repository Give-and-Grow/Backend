from flask import Blueprint, request, jsonify
from app.services.notification_service import notify_user
from app.models import Account
from firebase_admin import firestore
from app.config import db_firestore
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db

notification_bp = Blueprint("notification", __name__)
user_bp = Blueprint("user", __name__)

@user_bp.post("/fcm-token")
@jwt_required()
def update_fcm_token():
    user_id = get_jwt_identity()
    data = request.get_json()
    token = data.get("fcm_token")

    if not token:
        return jsonify({"error": "Missing FCM token"}), 400

    account = Account.query.get(user_id)
    if not account:
        return jsonify({"error": "User not found"}), 404

    account.fcm_token = token
    db.session.commit()
    return jsonify({"message": "FCM token updated"}), 200



@notification_bp.get("/list")
@jwt_required()
def list_notifications():
    user_id = get_jwt_identity()
    notifications_ref = db_firestore.collection("notifications").document(str(user_id)).collection("items")

    notifications = notifications_ref.order_by("created_at", direction=firestore.Query.DESCENDING).stream()

    notification_list = []
    for notif in notifications:
        notif_data = notif.to_dict()
        notif_data["id"] = notif.id

        
        from_user_id = notif_data.get("from_user")
        if from_user_id:
            sender = Account.query.get(from_user_id)
            if sender:
                notif_data["from_user_name"] = sender.username  # أو sender.full_name حسب جدولك

        notification_list.append(notif_data)

    return jsonify(notification_list), 200


@notification_bp.post("/mark-seen")
@jwt_required()
def mark_notification_seen():
    user_id = get_jwt_identity()
    data = request.get_json()
    notification_id = data.get("notification_id")

    if not notification_id:
        return jsonify({"error": "Notification ID is required"}), 400

    notif_ref = db_firestore.collection("notifications").document(str(user_id)).collection("items").document(notification_id)

    if not notif_ref.get().exists:
        return jsonify({"error": "Notification not found"}), 404

    notif_ref.update({"seen": True})
    return jsonify({"message": "Notification marked as seen"}), 200


@notification_bp.post("/mark-all-seen")
@jwt_required()
def mark_all_notifications_seen():
    user_id = get_jwt_identity()
    notifications_ref = db_firestore.collection("notifications").document(str(user_id)).collection("items")

    notifications = notifications_ref.where("seen", "==", False).stream()

    for notif in notifications:
        notif_ref = notifications_ref.document(notif.id)
        notif_ref.update({"seen": True})

    return jsonify({"message": "All notifications marked as seen"}), 200


@notification_bp.get("/unseen-count")
@jwt_required()
def unseen_notifications_count():
    user_id = get_jwt_identity()
    notifications_ref = db_firestore.collection("notifications").document(str(user_id)).collection("items")

    unseen_count = notifications_ref.where("seen", "==", False).get()

    return jsonify({"unseen_count": len(unseen_count)}), 200


@notification_bp.get("/unseen")
@jwt_required()
def unseen_notifications():
    user_id = get_jwt_identity()
    notifications_ref = db_firestore.collection("notifications").document(str(user_id)).collection("items")

    unseen_notifications = notifications_ref.where("seen", "==", False).order_by("created_at", direction=firestore.Query.DESCENDING).stream()

    notification_list = []
    for notif in unseen_notifications:
        notif_data = notif.to_dict()
        notif_data["id"] = notif.id
        notification_list.append(notif_data)

    return jsonify(notification_list), 200


@notification_bp.get("/seen")
@jwt_required()
def seen_notifications():
    user_id = get_jwt_identity()
    notifications_ref = db_firestore.collection("notifications").document(str(user_id)).collection("items")

    seen_notifications = notifications_ref.where("seen", "==", True).order_by("created_at", direction=firestore.Query.DESCENDING).stream()

    notification_list = []
    for notif in seen_notifications:
        notif_data = notif.to_dict()
        notif_data["id"] = notif.id
        notification_list.append(notif_data)

    return jsonify(notification_list), 200


@notification_bp.get("/count")
@jwt_required()
def notifications_count():
    user_id = get_jwt_identity()
    notifications_ref = db_firestore.collection("notifications").document(str(user_id)).collection("items")

    total_count = notifications_ref.get()

    return jsonify({"total_count": len(total_count)}), 200
