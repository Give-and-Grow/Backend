# app/services/post_service.py
from datetime import datetime
from app.config import db_firestore
import uuid
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from firebase_admin import firestore
from app.services.follow_service import get_following  # حسب مكان دالتك


db_firestore = firestore.client()

def create_post(user_id, title, content=None, tags=None, images=None):
    post_id = str(uuid.uuid4())
    post_data = {
        "post_id": post_id,
        "user_id": user_id,
        "title": title,
        "content": content or "",
        "tags": tags or [],
        "images": images or [],
        "created_at": datetime.utcnow(),
    }
    db_firestore.collection("posts").document(post_id).set(post_data)
    return {"message": "Post created successfully", "post_id": post_id}

def get_user_posts(user_id):
    posts_ref = db_firestore.collection('posts')
    docs = posts_ref.where("user_id", "==", user_id).order_by("created_at", direction="DESCENDING").stream()

    posts = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        data["created_at"] = data.get("created_at").isoformat() if data.get("created_at") else None
        data["is_mine"] = True  # لأنه كلهم لهذا اليوزر
        posts.append(data)

    return posts   

def delete_post(post_id, user_id):
    post_ref = db_firestore.collection('posts').document(post_id)
    post = post_ref.get()

    if not post.exists:
        return {"error": "Post not found"}, 404

    post_data = post.to_dict()
    if post_data["user_id"] != user_id:
        return {"error": "Unauthorized"}, 403

    post_ref.delete()
    return {"message": "Post deleted successfully"}

def update_post(post_id, user_id, updated_data):
    post_ref = db_firestore.collection('posts').document(post_id)
    post = post_ref.get()

    if not post.exists:
        return {"error": "Post not found"}, 404

    post_data = post.to_dict()
    if post_data["user_id"] != user_id:
        return {"error": "Unauthorized"}, 403

    updated_data["updated_at"] = firestore.SERVER_TIMESTAMP
    post_ref.update(updated_data)

    return {"message": "Post updated successfully"}

def add_comment(post_id, user_id, content):
    post_ref = db_firestore.collection("posts").document(post_id)
    if not post_ref.get().exists:
        return {"error": "Post not found"}, 404

    comment_ref = post_ref.collection("comments").document()
    comment_data = {
        "user_id": user_id,
        "content": content,
        "created_at": firestore.SERVER_TIMESTAMP
    }
    comment_ref.set(comment_data)

    return {"message": "Comment added", "comment_id": comment_ref.id}

def get_comments(post_id, user_id):
    comments_ref = db_firestore.collection("posts").document(post_id).collection("comments").order_by("created_at")
    comments = comments_ref.stream()

    post_doc = db_firestore.collection("posts").document(post_id).get()
    post_owner_id = post_doc.to_dict().get("user_id") if post_doc.exists else None

    result = []
    for comment in comments:
        data = comment.to_dict()
        data["id"] = comment.id
        data["is_mine"] = (data["user_id"] == user_id)
        data["is_post_owner"] = (post_owner_id == user_id)
        result.append(data)

    return result


def delete_comment(post_id, comment_id, user_id):
    post_ref = db_firestore.collection("posts").document(post_id)
    comment_ref = post_ref.collection("comments").document(comment_id)

    comment_doc = comment_ref.get()
    if not comment_doc.exists:
        return {"error": "Comment not found"}, 404

    comment_data = comment_doc.to_dict()
    post_doc = post_ref.get()
    if not post_doc.exists:
        return {"error": "Post not found"}, 404
    post_owner_id = post_doc.to_dict().get("user_id")

    if comment_data["user_id"] != user_id and post_owner_id != user_id:
        return {"error": "Not authorized to delete this comment"}, 403

    comment_ref.delete()
    return {"message": "Comment deleted"}

def edit_comment(post_id, comment_id, user_id, new_content):
    comment_ref = db_firestore.collection("posts").document(post_id).collection("comments").document(comment_id)
    comment_doc = comment_ref.get()

    if not comment_doc.exists:
        return {"error": "Comment not found"}, 404

    comment_data = comment_doc.to_dict()

    if comment_data["user_id"] != user_id:
        return {"error": "Not authorized to edit this comment"}, 403

    comment_ref.update({
        "content": new_content
    })

    return {"message": "Comment updated"}

def get_following_posts(user_id):
    following = get_following(user_id)  
    print("Following list:", get_following(user_id))
    following_ids = [f['id'] for f in following]


    posts_ref = db_firestore.collection('posts')
    posts = []

    for uid in following_ids:
        docs = posts_ref.where("user_id", "==", str(uid)).order_by("created_at", direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            created_at = data.get('created_at')
            data['created_at'] = created_at.isoformat() if isinstance(created_at, datetime) else created_at
            posts.append(data)

    posts.sort(key=lambda x: x['created_at'], reverse=True)
    return posts