import enum
from datetime import datetime
from sqlalchemy import DateTime, Enum, func
from ..extensions import db


class AchievementType(enum.Enum):
    GENERAL = "general"
    DISCOUNT = "discount"
    RANKING = "ranking"

class Ranking(enum.Enum):
    PLATINUM = "Platinum"
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"

class Level(enum.Enum):
    LEVEL_1 = "l1"
    LEVEL_2 = "l2"
    LEVEL_3 = "l3"
    LEVEL_4 = "l4"

   

class UserAchievement(db.Model):
    __tablename__ = "user_achievement"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_details.id"), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    badge_icon = db.Column(db.String(255))

    achievement_type = db.Column(db.Enum(AchievementType), default=AchievementType.GENERAL, nullable=False)

    points = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Enum(Level), nullable=True)
    ranking = db.Column(db.Enum(Ranking), nullable=True)

    event_date = db.Column(DateTime, nullable=False, default=func.now())  

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Achievement {self.title} ({self.achievement_type.value}) for User {self.user_id} on {self.event_date}>"
