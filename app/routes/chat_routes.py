from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.chat_service import *
from app.utils.decorators import organization_required
from sqlalchemy.orm import joinedload
from app.models.account import Account, Role

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("/opportunity/<int:opportunity_id>/create", methods=["POST"])
@jwt_required()
@organization_required
def create_chat(opportunity_id):
    try:
        chat = create_chat_for_opportunity(opportunity_id)
        return jsonify({"message": "Chat created", "chat_id": chat.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@chat_bp.route("/opportunity/<int:opportunity_id>/send", methods=["POST"])
@jwt_required()
def send_message(opportunity_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get("message")

    try:
        send_message_to_opportunity_chat(opportunity_id, user_id, content)
        return jsonify({"message": "Message sent"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500

@chat_bp.route("/opportunity/<int:opportunity_id>/messages", methods=["GET"])
@jwt_required()
def get_chat_messages(opportunity_id):
    try:
        messages = get_chat_messages_service(opportunity_id)
        return jsonify({"messages": messages}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400        

@chat_bp.route("/opportunity/<int:opportunity_id>/message/<string:message_id>", methods=["DELETE"])
@jwt_required()
def delete_chat_message(opportunity_id, message_id):
    user_id = get_jwt_identity()
    try:
        delete_message_service(opportunity_id, message_id, user_id)
        return jsonify({"message": "Message deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@chat_bp.route("/opportunity/<int:opportunity_id>/message/<string:message_id>", methods=["PUT"])
@jwt_required()
def edit_chat_message(opportunity_id, message_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    new_content = data.get("new_content")

    try:
        edit_message_service(opportunity_id, message_id, user_id, new_content)
        return jsonify({"message": "Message updated successfully."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@chat_bp.get("/my-organization-chats")
@jwt_required()
def get_my_organization_chats():
    current_user_id = get_jwt_identity()
    
    try:
        account = Account.query.get(current_user_id)
        if account.role != Role.ORGANIZATION:
            return jsonify({"error": "Only organizations can access this route."}), 403

        chats = get_organization_chats(current_user_id)
        return jsonify(chats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@chat_bp.get("/my-user-chats")
@jwt_required()
def get_my_user_chats():
    current_user_id = get_jwt_identity()

    try:
        account = Account.query.get(current_user_id)
        if account.role != Role.USER:
            return jsonify({"error": "Only users can access this route."}), 403

        chats = get_user_chats(current_user_id)
        return jsonify(chats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@chat_bp.put("/lock-chat/<int:opportunity_id>")
@jwt_required()
def lock_chat(opportunity_id):
    current_user_id = int(get_jwt_identity())
    opportunity = Opportunity.query.options(joinedload(Opportunity.organization)).filter_by(id=opportunity_id).first()

    if not opportunity or opportunity.organization.account_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        toggle_chat_lock(opportunity_id, lock=True)
        return jsonify({"message": "Chat locked"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@chat_bp.put("/unlock-chat/<int:opportunity_id>")
@jwt_required()
def unlock_chat(opportunity_id):
    current_user_id = int(get_jwt_identity())
    opportunity = Opportunity.query.options(joinedload(Opportunity.organization)).filter_by(id=opportunity_id).first()

    if not opportunity or opportunity.organization.account_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        toggle_chat_lock(opportunity_id, lock=False)
        return jsonify({"message": "Chat unlocked"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_account_role(account_id):
    account = Account.query.get(account_id)
    if not account:
        return None
    return account.role.name  

@chat_bp.route("/search-chats", methods=["GET"])
@jwt_required()
def search_chats():
    current_user_id = get_jwt_identity()
    query = request.args.get("q")

    if not query:
        return jsonify({"msg": "Search query is required"}), 400

    account = Account.query.get(current_user_id)
    
    if not account:
        return jsonify({"msg": "Account not found"}), 404

    if account.role == Role.ORGANIZATION:
        chats = get_organization_chats(current_user_id)
    else:
        chats = get_user_chats(current_user_id)

    filtered_chats = [
        chat for chat in chats
        if query.lower() in chat["opportunity_title"].lower()
    ]

    return jsonify(filtered_chats), 200
