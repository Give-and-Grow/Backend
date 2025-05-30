from firebase_admin import firestore
from app.models import OpportunityChat, OpportunityParticipant, ParticipantStatus, Opportunity
from app.extensions import db
from app.models import UserDetails
from app.models.account import Account ,Role
from app.models.user_details import UserDetails
from app.models.organization_details import OrganizationDetails
from datetime import datetime, timezone, timedelta

db_firestore = firestore.client()



def create_chat_for_opportunity(opportunity_id):
    existing = OpportunityChat.query.filter_by(opportunity_id=opportunity_id).first()
    if existing:
        raise Exception("Chat already exists.")

    chat = OpportunityChat(opportunity_id=opportunity_id)
    db.session.add(chat)
    db.session.commit()

    chat_doc = f"opportunity_{opportunity_id}"
    db_firestore.collection("chats").document(chat_doc).set({
        "created_at": firestore.SERVER_TIMESTAMP,
        "opportunity_id": opportunity_id,
        "is_locked": False
    })

    accepted_participants = OpportunityParticipant.query.filter_by(
        opportunity_id=opportunity_id,
        status=ParticipantStatus.ACCEPTED
    ).all()

    for participant in accepted_participants:
        user_details = UserDetails.query.get(participant.user_id)
        if user_details:
            account_id = user_details.account_id
            db_firestore.collection("chats").document(chat_doc).collection("members").document(str(account_id)).set({
                "joined_at": firestore.SERVER_TIMESTAMP
            })

    # إضافة المؤسسة مالكة الفرصة
    opportunity = Opportunity.query.get(opportunity_id)
    if opportunity and opportunity.organization:
        org_account_id = opportunity.organization.account_id
        db_firestore.collection("chats").document(chat_doc).collection("members").document(str(org_account_id)).set({
            "joined_at": firestore.SERVER_TIMESTAMP
        })

    return chat




def add_user_to_chat_if_exists(opportunity_id, user_id):
    chat = OpportunityChat.query.filter_by(opportunity_id=opportunity_id).first()
    if not chat:
        return

    chat_doc = f"opportunity_{opportunity_id}"

    # user_id هنا هو Account.id، بس Firebase عنده الـ members مخزنين بالـ account_id
    db_firestore.collection("chats").document(chat_doc).collection("members").document(str(user_id)).set({
        "joined_at": firestore.SERVER_TIMESTAMP
    })


def send_message_to_opportunity_chat(opportunity_id, user_id, content):
    if not content:
        raise ValueError("Message content is required")

    chat = OpportunityChat.query.filter_by(opportunity_id=opportunity_id).first()
    if not chat:
        raise ValueError("Chat does not exist for this opportunity")

    from app.models import UserDetails
    user_details = UserDetails.query.filter_by(account_id=user_id).first()
    user_details_id = user_details.id if user_details else None

    is_member = OpportunityParticipant.query.filter_by(
        opportunity_id=opportunity_id,
        user_id=user_details_id,
        status=ParticipantStatus.ACCEPTED
    ).first() or chat.opportunity.organization.account_id == user_id

    if not is_member:
        raise PermissionError("User is not allowed to send messages in this chat")

    chat_doc = f"opportunity_{opportunity_id}"
    chat_meta = db_firestore.collection("chats").document(chat_doc).get()
    
    # ✅ تحقق مما إذا كانت المحادثة مقفلة
    if chat_meta.exists and chat_meta.to_dict().get("is_locked"):
        raise PermissionError("This chat is currently locked. No messages can be sent.")

    db_firestore.collection("chats").document(chat_doc).collection("messages").add({
        "user_id": user_id,
        "content": content,
        "sent_at": firestore.SERVER_TIMESTAMP
    })


def get_chat_messages_service(opportunity_id):
    chat_doc = f"opportunity_{opportunity_id}"
    messages_ref = db_firestore.collection("chats").document(chat_doc).collection("messages")
    docs = messages_ref.order_by("sent_at").stream()

    messages = []
    for doc in docs:
        msg_data = doc.to_dict()
        user_id = int(msg_data.get("user_id"))  # جربت تحويله للـ int

        # جلب حساب المستخدم
        account = Account.query.get(user_id)
        if not account:
            # إذا الحساب مش موجود، حط بيانات افتراضية أو تجاهل الرسالة
            msg_data["sender_name"] = "Unknown"
            msg_data["sender_profile_picture"] = None
        else:
            if account.role == Role.USER:
                details = UserDetails.query.filter_by(account_id=user_id).first()
                if details:
                    sender_name = f"{details.first_name} {details.last_name}"
                    sender_profile_picture = details.profile_picture
                else:
                    sender_name = account.username or account.email
                    sender_profile_picture = None

            elif account.role == Role.ORGANIZATION:
                details = OrganizationDetails.query.filter_by(account_id=user_id).first()
                if details:
                    sender_name = details.name
                    sender_profile_picture = details.logo
                else:
                    sender_name = account.username or account.email
                    sender_profile_picture = None
            else:
                # للإدارة أو أدوار أخرى
                sender_name = account.username or account.email
                sender_profile_picture = None

            msg_data["sender_name"] = sender_name
            msg_data["sender_profile_picture"] = sender_profile_picture
            if "edited_at" in msg_data:
                msg_data["is_edited"] = True
            else:
                msg_data["is_edited"] = False    

        msg_data["id"] = doc.id
        messages.append(msg_data)

    return messages

def delete_message_service(opportunity_id, message_id, current_user_id):
    chat_doc = f"opportunity_{opportunity_id}"
    message_ref = db_firestore.collection("chats").document(chat_doc).collection("messages").document(message_id)

    message_doc = message_ref.get()
    if not message_doc.exists:
        raise Exception("Message not found.")

    
    message_data = message_doc.to_dict()
    print("Current User ID:", current_user_id, "Type:", type(current_user_id))
    print("Sender ID from message:", message_data.get("user_id"), "Type:", type(message_data.get("user_id")))

    if str(message_data.get("user_id")) != str(current_user_id):
        raise Exception("You are not authorized to delete this message.")

    message_ref.delete()
    return True

def edit_message_service(opportunity_id, message_id, current_user_id, new_content):
    if not new_content or len(new_content.strip()) == 0:
        raise ValueError("Message content cannot be empty.")

    chat_doc = f"opportunity_{opportunity_id}"
    message_ref = db_firestore.collection("chats").document(chat_doc).collection("messages").document(message_id)

    message_doc = message_ref.get()
    if not message_doc.exists:
        raise Exception("Message not found.")

    message_data = message_doc.to_dict()

    # تأكد إن المستخدم هو صاحب الرسالة
    if str(message_data.get("user_id")) != str(current_user_id):
        raise Exception("You are not authorized to edit this message.")

    # تحقق من وقت الإرسال
    sent_at = message_data.get("sent_at")
    if not sent_at:
        raise Exception("Message timestamp is missing.")

    now = datetime.now(timezone.utc)
    if isinstance(sent_at, datetime):
        time_diff = now - sent_at
        if time_diff > timedelta(minutes=10):
            raise Exception("You can only edit a message within 10 minutes of sending it.")
    else:
        raise Exception("Invalid timestamp format.")

    # عدّل الرسالة
    message_ref.update({
        "content": new_content,
        "edited_at": firestore.SERVER_TIMESTAMP
    })

    return True


def edit_message_service(opportunity_id, message_id, current_user_id, new_content):
    if not new_content or len(new_content.strip()) == 0:
        raise ValueError("Message content cannot be empty.")

    chat_doc = f"opportunity_{opportunity_id}"
    message_ref = db_firestore.collection("chats").document(chat_doc).collection("messages").document(message_id)

    message_doc = message_ref.get()
    if not message_doc.exists:
        raise Exception("Message not found.")

    message_data = message_doc.to_dict()

    if str(message_data.get("user_id")) != str(current_user_id):
        raise Exception("You are not authorized to edit this message.")

    sent_at = message_data.get("sent_at")
    if not sent_at:
        raise Exception("Message timestamp is missing.")

    # 🔁 تأكد أن sent_at هو datetime وليس string
    if isinstance(sent_at, str):
        sent_at = datetime.strptime(sent_at, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    time_diff = now - sent_at
    if time_diff > timedelta(minutes=10):
        raise Exception("You can only edit a message within 10 minutes of sending it.")

    message_ref.update({
        "content": new_content,
        "edited_at": firestore.SERVER_TIMESTAMP
    })

    return True

def get_organization_chats(account_id):
    # أولاً نجيب الفرص تبعت المؤسسة
    organization = OrganizationDetails.query.filter_by(account_id=account_id).first()
    if not organization:
        raise Exception("Organization not found.")

    opportunities = Opportunity.query.filter_by(organization_id=organization.id).all()
    opportunity_ids = [op.id for op in opportunities]

    chat_list = []
    for opp_id in opportunity_ids:
        chat_doc_id = f"opportunity_{opp_id}"
        chat_ref = db_firestore.collection("chats").document(chat_doc_id)
        chat_doc = chat_ref.get()

        if chat_doc.exists:
            chat_data = chat_doc.to_dict()
            chat_data["chat_id"] = chat_doc_id
            chat_data["opportunity_id"] = opp_id
            chat_data["opportunity_title"] = Opportunity.query.get(opp_id).title
            chat_list.append(chat_data)

    return chat_list

def get_user_chats(account_id):
    user_details = UserDetails.query.filter_by(account_id=account_id).first()
    if not user_details:
        raise Exception("User details not found.")

    # نجيب كل الفرص اللي مقبول فيها
    accepted_participations = OpportunityParticipant.query.filter_by(
        user_id=user_details.id,
        status=ParticipantStatus.ACCEPTED
    ).all()

    opportunity_ids = [p.opportunity_id for p in accepted_participations]

    chat_list = []
    for opp_id in opportunity_ids:
        chat_doc_id = f"opportunity_{opp_id}"
        chat_ref = db_firestore.collection("chats").document(chat_doc_id)
        chat_doc = chat_ref.get()

        if chat_doc.exists:
            chat_data = chat_doc.to_dict()
            chat_data["chat_id"] = chat_doc_id
            chat_data["opportunity_id"] = opp_id
            chat_data["opportunity_title"] = Opportunity.query.get(opp_id).title
            chat_data["is_locked"] = chat_data.get("is_locked", False)
            chat_list.append(chat_data)

    return chat_list

def toggle_chat_lock(opportunity_id, lock=True):
    chat_doc = f"opportunity_{opportunity_id}"
    chat_ref = db_firestore.collection("chats").document(chat_doc)

    if not chat_ref.get().exists:
        raise Exception("Chat not found.")

    chat_ref.update({"is_locked": lock})
    return True
