# app/routes/post_routes.py
from flask import Blueprint, request, jsonify, g
from app.services.post_service import *
from app.utils.decorators import account_required

post_bp = Blueprint("post", __name__)

@post_bp.post("/")
@account_required
def create_new_post():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags", [])
    images = data.get("images", [])

    if not title:
        return jsonify({"error": "Title is required"}), 400

    result = create_post(
        user_id=g.user_id,
        title=title,
        content=content,
        tags=tags,
        images=images,
    )
    return jsonify(result), 201

@post_bp.get('/')
@account_required
def fetch_posts():
    return jsonify(get_user_posts(g.user_id))    

@post_bp.put('/<post_id>')
@account_required
def update_post_route(post_id):
    data = request.get_json()
    return jsonify(update_post(post_id, g.user_id, data))

@post_bp.delete('/<post_id>')
@account_required
def delete_post_route(post_id):
    return jsonify(delete_post(post_id, g.user_id))

@post_bp.post('/<post_id>/comments')
@account_required
def add_comment_route(post_id):
    data = request.get_json()
    return jsonify(add_comment(post_id, g.user_id, data["content"]))

@post_bp.get('/<post_id>/comments')
@account_required
def get_comments_route(post_id):
    return jsonify(get_comments(post_id, g.user_id))

@post_bp.put('/<post_id>/comments/<comment_id>')
@account_required
def edit_comment_route(post_id, comment_id):
    data = request.get_json()
    return jsonify(edit_comment(post_id, comment_id, g.user_id, data["content"]))

@post_bp.delete('/<post_id>/comments/<comment_id>')
@account_required
def delete_comment_route(post_id, comment_id):
    return jsonify(delete_comment(post_id, comment_id, g.user_id))

@post_bp.route("/following", methods=["GET"])
@account_required
def posts_from_following():
    current_user_id = g.user_id
    posts = get_following_posts(current_user_id)
    return jsonify(posts), 200

@post_bp.get('/<post_id>')
@account_required
def get_single_post(post_id):
    result = get_post_by_id(post_id, current_user_id=g.user_id)
    if isinstance(result, tuple):  # في حال رجع (dict, status_code)
        return jsonify(result[0]), result[1]
    return jsonify(result), 200