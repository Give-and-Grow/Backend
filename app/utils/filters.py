from app.models.opportunity import OpportunityStatus

def filter_available_opportunities(opportunities):
    return [
        opp for opp in opportunities
        if opp.get("is_deleted") in [False, 0] and opp.get("status") == "OPEN"
    ]