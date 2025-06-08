import datetime
from firebase_admin import firestore
from uuid import uuid4

db = firestore.client()
ADS_COLLECTION = "promotional_ads"

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
    db.collection(ADS_COLLECTION).document(ad_id).set(ad_data)
    return ad_id


def get_all_ads():
    ads = db.collection(ADS_COLLECTION).stream()
    return [{**ad.to_dict(), "id": ad.id} for ad in ads]


def get_ad_by_id(ad_id):
    doc = db.collection(ADS_COLLECTION).document(ad_id).get()
    if doc.exists:
        return {**doc.to_dict(), "id": doc.id}
    return None


def update_ad(ad_id, data):
    doc_ref = db.collection(ADS_COLLECTION).document(ad_id)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    update_data = {**data, "updated_at": datetime.datetime.utcnow().isoformat()}
    doc_ref.update(update_data)
    return True


def delete_ad(ad_id):
    doc_ref = db.collection(ADS_COLLECTION).document(ad_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True
