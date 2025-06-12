import datetime
from uuid import uuid4
from firebase_admin import firestore
from app.utils.email import send_ad_status_email
from app.config import db_firestore

db = firestore.client()
ADS_COLLECTION = "promotional_ads"
ADS_REQUEST_COLLECTION = "ads_requests"

def create_ad(data):
    ad_id = str(uuid4())
    now = datetime.datetime.utcnow().isoformat()
    ad_data = {
        "store_name": data["store_name"],
        "image_url": data["image_url"],
        "description": data.get("description"),
        "website_url": data.get("website_url"),
        "is_active": data.get("is_active", True),
        "created_at": now,
        "updated_at": now
    }
    db_firestore.collection(ADS_COLLECTION).document(ad_id).set(ad_data)
    return ad_id

def get_all_ads():
    ads = db_firestore.collection(ADS_COLLECTION).stream()
    return [{**ad.to_dict(), "id": ad.id} for ad in ads]

def get_ad_by_id(ad_id):
    doc = db_firestore.collection(ADS_COLLECTION).document(ad_id).get()
    if doc.exists:
        return {**doc.to_dict(), "id": doc.id}
    return None

def update_ad(ad_id, data):
    doc_ref = db_firestore.collection(ADS_COLLECTION).document(ad_id)
    if not doc_ref.get().exists:
        return False
    data["updated_at"] = datetime.datetime.utcnow().isoformat()
    doc_ref.update(data)
    return True

def delete_ad(ad_id):
    doc_ref = db_firestore.collection(ADS_COLLECTION).document(ad_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True

def submit_ad_request_service(data):
    ad_id = str(uuid4())
    now = datetime.datetime.utcnow().isoformat()
    ad_data = {
        "store_name": data["store_name"],
        "image_url": data["image_url"],
        "description": data["description"],
        "website_url": data["website_url"],
        "email": data["email"],
        "submitted_at": now,
        "status": "pending",
        "response_message": None
    }
    db_firestore.collection(ADS_REQUEST_COLLECTION).document(ad_id).set(ad_data)
    return ad_id

def get_pending_ads_service():
    requests = db_firestore.collection(ADS_REQUEST_COLLECTION).where("status", "==", "pending").stream()
    return [{**r.to_dict(), "id": r.id} for r in requests]

def approve_ad_service(ad_id):
    doc_ref = db_firestore.collection(ADS_REQUEST_COLLECTION).document(ad_id)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    data = doc.to_dict()
    now = datetime.datetime.utcnow().isoformat()

    final_ad = {
        "store_name": data["store_name"],
        "image_url": data["image_url"],
        "description": data["description"],
        "website_url": data["website_url"],
        "created_at": now,
        "updated_at": now,
        "is_active": True,
        "ad_source": "user"
    }

    db_firestore.collection(ADS_COLLECTION).document(str(uuid4())).set(final_ad)
    doc_ref.update({"status": "approved"})
    send_ad_status_email(data["email"], "accepted", data["store_name"])
    return True

def reject_ad_service(ad_id, reason):
    doc_ref = db_firestore.collection(ADS_REQUEST_COLLECTION).document(ad_id)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    data = doc.to_dict()
    doc_ref.update({"status": "rejected", "response_message": reason})
    send_ad_status_email(data["email"], "rejected", data["store_name"], reason)
    return True
