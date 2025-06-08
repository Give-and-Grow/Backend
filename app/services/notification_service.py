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

import requests

FCM_API_URL = 'https://fcm.googleapis.com/fcm/send'
FCM_SERVER_KEY = 'AIzaSyDWacP5kjQRrXPxIAgu05sg0iVn6YOjeeQ'

def send_push_notification(fcm_token, title, body):
    headers = {
        'Authorization': f'key={FCM_SERVER_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        "to": fcm_token,
        "notification": {
            "title": title,
            "body": body
        },
        "priority": "high"
    }

    response = requests.post(FCM_API_URL, headers=headers, json=data)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)  # راح يوضح السبب
    try:
        response_json = response.json()
    except Exception as e:
        print("Error decoding JSON:", e)
        response_json = None
    return response.status_code, response_json
