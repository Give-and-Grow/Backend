from firebase_admin import messaging
from google.cloud import firestore
from app.config import db_firestore

def send_firebase_notification(user_fcm_token, user_id, title, body, data=None):
    try:
        # 1. تأكد من أن مفاتيح data صالحة للإرسال لـ FCM (غيرنا "from" إلى "from_user")
        raw_data = data or {}
        cleaned_data = {("from_user" if k == "from" else k): str(v) for k, v in raw_data.items()}

        # 2. إرسال الإشعار عبر FCM
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=user_fcm_token,
            data=cleaned_data
        )
        response = messaging.send(message)
        print(f"Notification sent to {user_id}, FCM response: {response}")

        # 3. تخزين الإشعار في Firestore
        notif_ref = db_firestore.collection("notifications").document(str(user_id)).collection("items").document()
        notif_ref.set({
            "title": title,
            "body": body,
            "type": cleaned_data.get("type", "general"),
            "from_user": cleaned_data.get("from_user"),
            "seen": False,
            "created_at": firestore.SERVER_TIMESTAMP,
            **cleaned_data
        })

    except Exception as e:
        print(f"Error sending notification: {e}")
