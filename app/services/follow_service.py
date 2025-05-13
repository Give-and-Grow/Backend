from app.models.follow import  Follow
from app.models.account import Account, Role
from app.models.user_details import UserDetails
from app.models.organization_details import OrganizationDetails
from sqlalchemy.exc import IntegrityError
from app.extensions import db

def follow_user(follower_id, followed_id):
    if follower_id == followed_id:
        return {'error': "You can't follow yourself"}, 400

    existing = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if existing:
        return {'message': "Already following"}, 200

    follow = Follow(follower_id=follower_id, followed_id=followed_id)
    db.session.add(follow)
    try:
        db.session.commit()
        return {'message': "Followed successfully"}, 201
    except IntegrityError:
        db.session.rollback()
        return {'error': "Follow action failed"}, 500


def unfollow_user(follower_id, followed_id):
    follow = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if not follow:
        return {'error': "Not following"}, 404

    db.session.delete(follow)
    db.session.commit()
    return {'message': "Unfollowed successfully"}, 200


def get_following(user_id):
    follows = Follow.query.filter_by(follower_id=user_id).all()
    following_list = []
    
    for f in follows:
        followed_account = f.followed_account
        if followed_account.role == "user":  # إذا كان الحساب من نوع مستخدم
            profile_picture = followed_account.user_details.profile_picture if followed_account.user_details else None
        elif followed_account.role == "organization":  # إذا كان الحساب من نوع مؤسسة
            profile_picture = followed_account.organization_details.logo if followed_account.organization_details else None
        else:
            profile_picture = None
        
        following_list.append({
            'id': followed_account.id,
            'username': followed_account.username,
            'profile_picture': profile_picture
        })
    
    return following_list


def get_followers(user_id):
    followers = Follow.query.filter_by(followed_id=user_id).all()
    followers_list = []

    for f in followers:
        follower_account = f.follower_account  # ✅ استخدم الاسم الصحيح
        if follower_account.role == Role.USER:
            profile_picture = follower_account.user_details.profile_picture if follower_account.user_details else None
        elif follower_account.role == Role.ORGANIZATION:
            profile_picture = follower_account.organization_details.logo if follower_account.organization_details else None
        else:
            profile_picture = None

        followers_list.append({
            'id': follower_account.id,
            'username': follower_account.username,
            'profile_picture': profile_picture
        })

    return followers_list



def is_following(follower_id, followed_id):
    return Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first() is not None
