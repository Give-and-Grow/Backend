from datetime import date, datetime
from decimal import Decimal
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.participant_evaluation import ParticipantEvaluation
from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.models.opportunity import Opportunity
from app.extensions import db
from app.models.user_points import UserPoints
from app.models import *
from app.services.post_service import *


from datetime import datetime, date, timedelta

def update_user_points_summary(user_id, db_session):
    print(f"🔁 Checking if we should update summary for user {user_id}")
    today = date.today()
    first_day_of_month = today.replace(day=1)
    first_day_of_year = today.replace(month=1, day=1)

    is_july_first = (today.month == 7 and today.day == 1)
    is_month_end = (today == (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1))
    is_year_end = (today.month == 12 and today.day == 31)

    if not (is_july_first or is_month_end or is_year_end):
        print("⛔ Not the right time to update summaries.")
        return

    print(f"✅ Proceeding to update summaries for user {user_id}...")

    # حساب النقاط الشهرية
    month_total = db_session.query(
        db.func.coalesce(db.func.sum(UserPoints.points_earned), 0)
    ).join(Opportunity).filter(
        UserPoints.user_id == user_id,
        Opportunity.date >= first_day_of_month
    ).scalar()
    print(f"📊 Monthly total: {month_total}")

    # حساب النقاط السنوية
    year_total = db_session.query(
        db.func.coalesce(db.func.sum(UserPoints.points_earned), 0)
    ).join(Opportunity).filter(
        UserPoints.user_id == user_id,
        Opportunity.date >= first_day_of_year
    ).scalar()
    print(f"📊 Yearly total: {year_total}")

    # 🔍 هل المستخدم هو الأعلى نقاطًا في الشهر أو السنة؟
    max_month_points = db_session.query(
        db.func.max(UserPointsSummary.total_points)
    ).filter(
        UserPointsSummary.period_type == PeriodType.MONTH,
        UserPointsSummary.period_start == first_day_of_month
    ).scalar() or 0

    max_year_points = db_session.query(
        db.func.max(UserPointsSummary.total_points)
    ).filter(
        UserPointsSummary.period_type == PeriodType.YEAR,
        UserPointsSummary.period_start == first_day_of_year
    ).scalar() or 0

    is_top_month = month_total >= max_month_points and is_month_end
    is_top_year = year_total >= max_year_points and (is_year_end or is_july_first)

    if is_top_month:
        print("🏆 User is top monthly scorer!")
        summary_month = UserPointsSummary.query.filter_by(
            user_id=user_id,
            period_type=PeriodType.MONTH,
            period_start=first_day_of_month,
            period_end=today
        ).first()
        if summary_month:
            summary_month.total_points = month_total
        else:
            summary_month = UserPointsSummary(
                user_id=user_id,
                period_type=PeriodType.MONTH,
                period_start=first_day_of_month,
                period_end=today,
                total_points=month_total
            )
            db_session.add(summary_month)
        user = UserDetails.query.filter_by(id=user_id).first()    
        account_id=user.account_id
        create_post(
            user_id=account_id,
            title="🎉 Top Volunteer of the Month!",
            content=f"Congratulations! You were the top scorer in volunteering points for {first_day_of_month.strftime('%B %Y')}! 🌟",
            tags=["TopVolunteer", "MonthlyWinner"]
        )    

    if is_top_year:
        print("🏆 User is top yearly scorer!")
        summary_year = UserPointsSummary.query.filter_by(
            user_id=user_id,
            period_type=PeriodType.YEAR,
            period_start=first_day_of_year,
            period_end=today
        ).first()
        if summary_year:
            summary_year.total_points = year_total
        else:
            summary_year = UserPointsSummary(
                user_id=user_id,
                period_type=PeriodType.YEAR,
                period_start=first_day_of_year,
                period_end=today,
                total_points=year_total
            )
            db_session.add(summary_year)
        user = UserDetails.query.filter_by(id=user_id).first()    
        account_id=user.account_id
        create_post(
            user_id=account_id,
            title="🏆 Top Volunteer of the Year!",
            content=f"Amazing! You achieved the highest volunteer score for the year {first_day_of_year.year}! 💪🎖️",
            tags=["TopVolunteer", "YearlyWinner"]
        )    

def create_or_update_achievement(user, db_session):
    print(f"🏆 Checking for existing achievement for user {user.id} with rank {user.rank}")

    existing = UserAchievement.query.filter_by(
        user_id=user.id,
        ranking=user.rank
    ).first()

    if existing:
        print(f"✅ Achievement already exists for rank: {user.rank}")
    else:
        print(f"➕ Creating new achievement for rank: {user.rank}")
        achievement = UserAchievement(
            user_id=user.id,
            title=f"{user.rank} Rank Achieved",
            description=f"Congratulations! You've achieved {user.rank} rank.",
            achievement_type=AchievementType.RANKING,
            ranking=Ranking[user.rank.upper()],
            points=user.total_points,
            event_date=datetime.utcnow()
        )
        db_session.add(achievement)

