from app.utils.decorators import account_required
from flask import Blueprint, jsonify, g
from flask_jwt_extended import get_jwt_identity
from app.services.follow_service import *

follow_bp = Blueprint('follow', __name__, url_prefix='/follow')

@follow_bp.post('/<int:user_id>')
@account_required
def follow(user_id):
    return jsonify(*follow_user(g.user_id, user_id))

@follow_bp.delete('/<int:user_id>')
@account_required
def unfollow(user_id):
    return jsonify(*unfollow_user(g.user_id, user_id))

@follow_bp.get('/followers')
@account_required
def get_my_followers():
    return jsonify(get_followers(g.user_id))

@follow_bp.get('/following')
@account_required
def get_my_following():
    return jsonify(get_following(g.user_id))

@follow_bp.get('/<int:user_id>/followers')
@account_required
def get_user_followers(user_id):
    return jsonify(get_followers(user_id))

@follow_bp.get('/<int:user_id>/following')
@account_required
def get_user_following(user_id):
    return jsonify(get_following(user_id))

@follow_bp.get('/<int:user_id>/is-following')
@account_required
def is_following_user(user_id):
    return jsonify({"is_following": is_following(g.user_id, user_id)})