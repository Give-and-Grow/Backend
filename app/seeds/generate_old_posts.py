from datetime import date, datetime
from flask import jsonify
from app.models.participant_evaluation import ParticipantEvaluation
from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.models.opportunity import Opportunity
from app.extensions import db
from app.models.user_points import UserPoints
from app.models import *
from app.services.post_service import *
from app import create_app  # 🆕

def generate_old_top_volunteer_posts():
    summaries = db.session.query(UserPointsSummary).all()

    for summary in summaries:
        print("hi")
        user_id = summary.user_id
        account = db.session.query(UserDetails).filter_by(id=user_id).first()
        if not account:
            continue

        account_id = account.account_id
        period_start = summary.period_start
        period_type = summary.period_type

        if period_type == PeriodType.MONTH:
            title = "🎉 Top Volunteer of the Month!"
            content = f"Congratulations! You were the top scorer in volunteering points for {period_start.strftime('%B %Y')}! 🌟"
            tags = ["TopVolunteer", "MonthlyWinner"]
        elif period_type == PeriodType.YEAR:
            title = "🏆 Top Volunteer of the Year!"
            content = f"Amazing! You achieved the highest volunteer score for the year {period_start.year}! 💪🎖️"
            tags = ["TopVolunteer", "YearlyWinner"]
        else:
            continue

        print(f"📢 Creating post for user {account_id} - {title}")
        create_post(
            user_id=str(account_id),
            title=title,
            content=content,
            tags=tags
        )

    print("✅ Done generating posts for old top volunteers.")

# ✅ تنفيذ داخل سياق التطبيق
app = create_app()
with app.app_context():
    generate_old_top_volunteer_posts()
