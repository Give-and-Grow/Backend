#GAG/app/services/dropdown_services.py
from app.models.opportunity import OpportunityStatus
from app.models.organization_details import VerificationStatus
from app.models.opportunity import OpportunityType
from app.models.account import Role
from app.models.admin_details import AdminRoleLevel
from app.models.industry import Industry
from app.models.opportunity_day import WeekDay
from app.models.opportunity_participant import ParticipantStatus
from app.models.opportunity import OpportunityStatus, OpportunityType
from app.models.organization_details import VerificationStatus
from app.models.participant_attendance import AttendanceStatus
from app.models.skill import Skill
from app.models.tag import Tag
from app.models.user_achievement import AchievementType, Level, Ranking
from app.models.user_details import Gender
from app.models.user_points import PeriodType
from app.extensions import db 

class DropdownService:

    @staticmethod
    def get_roles():
        return [{"label": role.name.title(), "value": role.value} for role in Role]
    
    @staticmethod
    def get_admin_roles():
        return [{"label": role.name.title(), "value": role.value} for role in AdminRoleLevel]
    
    @staticmethod
    def get_industries():
        industries = db.session.query(Industry).order_by(Industry.name).all()
        return [{"label": industry.name, "value": industry.id} for industry in industries]
    
    @staticmethod
    def get_week_days():
        return [{"label": day.name.title(), "value": day.value} for day in WeekDay]
    
    @staticmethod
    def get_participant_statuses():
        return [{"label": status.name.title(), "value": status.value} for status in ParticipantStatus]
    
    @staticmethod
    def get_opportunity_statuses():
        return [{"label": status.name.title(), "value": status.value} for status in OpportunityStatus]

    @staticmethod
    def get_opportunity_types():
        return [{"label": type_.name.title(), "value": type_.value} for type_ in OpportunityType]

    @staticmethod
    def get_verification_statuses():
        return [{"label": status.name.title(), "value": status.value} for status in VerificationStatus]
    
    @staticmethod
    def get_attendance_statuses():
        return [{"label": status.name.replace("_", " ").title(), "value": status.value} for status in AttendanceStatus]

    @staticmethod
    def get_skills():
        skills = db.session.query(Skill).order_by(Skill.name).all()
        return [{"label": skill.name, "value": skill.id} for skill in skills]
    @staticmethod
    def get_tags():
        tags = db.session.query(Tag).order_by(Tag.name).all()
        return [{"label": tag.name, "value": tag.id} for tag in tags]   

    @staticmethod
    def get_achievement_types():
        return [{"label": achievement_type.name.title(), "value": achievement_type.value} for achievement_type in AchievementType]

    @staticmethod
    def get_levels():
        return [{"label": level.name.title(), "value": level.value} for level in Level]

    @staticmethod
    def get_rankings():
        return [{"label": ranking.name.title(), "value": ranking.value} for ranking in Ranking]  

    @staticmethod
    def get_genders():
        return [{"label":gender.name.title(), "value"  :gender.value} for  gender in Gender] 
           
    @staticmethod
    def get_period_types():
        return [{"label": period_type.name.title(), "value": period_type.value} for period_type in PeriodType]



    # @staticmethod
    # def get_opportunity_status_options():
    #     return [status.value for status in OpportunityStatus]
        
    # @staticmethod
    # def get_opportunity_status_options():
    #     return [status.value for status in OpportunityStatus]

    # @staticmethod
    # def get_opportunity_type_options():
    #     return [type_.value for type_ in OpportunityType]

    # @staticmethod
    # def get_verification_status_options():
    #     return [status.value for status in VerificationStatus]



    # # @staticmethod
    # # def get_attendance_status_options():
    # #     return [status.value for status in AttendanceStatus]

        
