#Backend/app/services/dropdown_services.py
from app.models.opportunity import OpportunityStatus

class DropdownService:
    @staticmethod
    def get_opportunity_status_options():
        return [status.value for status in OpportunityStatus]
