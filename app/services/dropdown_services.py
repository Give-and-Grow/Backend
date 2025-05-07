#Backend/app/services/dropdown_services.py
from app.models.opportunity import OpportunityStatus
from app.models.opportunity_participant import AttendanceStatus
from app.models.report import ReportStatus
from app.models.organization_details import VerificationStatus
from app.models.opportunity import OpportunityType

class DropdownService:
    @staticmethod
    def get_opportunity_status_options():
        return [status.value for status in OpportunityStatus]
        
    @staticmethod
    def get_opportunity_status_options():
        return [status.value for status in OpportunityStatus]

    @staticmethod
    def get_opportunity_type_options():
        return [type_.value for type_ in OpportunityType]

    @staticmethod
    def get_verification_status_options():
        return [status.value for status in VerificationStatus]

    @staticmethod
    def get_report_status_options():
        return [status.value for status in ReportStatus]

    @staticmethod
    def get_attendance_status_options():
        return [status.value for status in AttendanceStatus]

        
