#Backend/service/notification_service.py
from app.models import Account
from app.utils.notifications import send_firebase_notification

def notify_user(user_id, title, body, data=None):
    account = Account.query.get(user_id)
    if not account or not account.fcm_token:
        print(f"FCM token not found for user {user_id}")
        return

    send_firebase_notification(
        user_fcm_token=account.fcm_token,
        user_id=user_id,
        title=title,
        body=body,
        data=data
    )

