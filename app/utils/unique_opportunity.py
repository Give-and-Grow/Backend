from app.models.opportunity import Opportunity



def generate_unique_opportunity_name(opportunity_name):
    existing_opportunity = Opportunity.query.filter_by(title=opportunity_name).first()

    if existing_opportunity:
        version = 1
        new_opportunity_name = f"{opportunity_name}_{version}"

        while Opportunity.query.filter_by(title=new_opportunity_name).first():
            version += 1
            new_opportunity_name = f"{opportunity_name}_{version}"

        return new_opportunity_name
    else:
        return opportunity_name
