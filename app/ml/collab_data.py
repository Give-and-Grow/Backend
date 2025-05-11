# Backend/app/ml/collab_data.py

from app.models.opportunity_participant import OpportunityParticipant
from app.models.volunteer_opportunity import VolunteerOpportunity
from app.extensions import db
import pandas as pd

def get_user_opportunity_interactions():
    data = []

    participants = OpportunityParticipant.query.all()

    for participant in participants:
        if not participant.completed or not participant.rating:
            continue  

        base_points = 100 
        volunteer_opp = VolunteerOpportunity.query.filter_by(opportunity_id=participant.opportunity_id).first()
        if volunteer_opp and volunteer_opp.base_points:
            base_points = volunteer_opp.base_points

        normalized_rating = round((participant.points_earned / base_points) * 5, 2)
        if normalized_rating > 5:
            normalized_rating = 5.0
        elif normalized_rating < 1:
            normalized_rating = 1.0

        data.append({
            "user_id": participant.user_id,
            "opportunity_id": participant.opportunity_id,
            "rating": normalized_rating
        })

    return data


def build_interaction_matrix():
    interactions = get_user_opportunity_interactions()

    df = pd.DataFrame(interactions)

    if df.empty:
        return None

    interaction_matrix = df.pivot_table(
        index='user_id',
        columns='opportunity_id',
        values='rating'
    )

    return interaction_matrix