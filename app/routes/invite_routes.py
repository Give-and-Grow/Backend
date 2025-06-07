from flask import Blueprint, jsonify
# from app.services.recommend_cf import recommend_users_for_org,invite_recommended_users
from app.models import ParticipantEvaluation, OpportunityParticipant, Opportunity,UserDetails, Account

from app.extensions import mail
from flask_mail import Message
invite_recommendation_bp = Blueprint("recommendation", __name__)

# @invite_recommendation_bp.route("/opportunity/<int:opportunity_id>", methods=["POST"])
# def invite_top_users(opportunity_id):

#     opportunity = Opportunity.query.get(opportunity_id)
#     if not opportunity:
#         return {"error": "Opportunity not found"}, 404

#     recommended = recommend_users_for_org(opportunity.organization_id, top_n=5)
#     print(recommended)
#     invite_recommended_users(opportunity_id, recommended)

#     return jsonify({"invited_user_ids": recommended})

from flask import jsonify
# from . import invite_recommendation_bp
from app.models import UserDetails

@invite_recommendation_bp.route("/opportunity/<int:opportunity_id>", methods=["GET"])
def invite_top_users(opportunity_id):
    # بدل التوصية، رجع أول 5 مستخدمين من الجدول
    users = UserDetails.query.limit(5).all()

    users_data = [
        {
            "id": user.account_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_picture": user.profile_picture,
            "total_points": user.total_points,
            "city": user.city,
            "country": user.country,
            "bio": user.bio
        }
        for user in users
    ]

    return jsonify({"invited_users": users_data})



@invite_recommendation_bp.route("/opportunity/<int:opportunity_id>", methods=["POST"])
def email_top_users(opportunity_id):
    # users = UserDetails.query.limit(5).all()

    # emails = []
    invited_users_data = []

    # for user in users:
    #     account = Account.query.get(user.account_id)
    #     if account and account.email:
    #         emails.append(account.email)
    #         invited_users_data.append({
    #             "id": user.account_id,
    #             "first_name": user.first_name,
    #             "last_name": user.last_name,
    #             "profile_picture": user.profile_picture,
    #             "total_points": user.total_points,
    #             "city": user.city,
    #             "country": user.country,
    #             "bio": user.bio,
    #             "email": account.email
    #         })

    # if emails:
    #     msg = Message(
    #         subject="🚀 You're Invited to a New Opportunity!",
    #         sender="your_email@gmail.com",
    #         recipients=[],  # نتركها فاضية
    #         bcc=emails,
    #         body="Hello,\n\nYou have been selected among the top users for a new opportunity. Visit GivAndGrow now to learn more!\n\nBest,\nGivAndGrow Team"
    #     )
    #     mail.send(msg)

    return jsonify({"invited_users": invited_users_data})
