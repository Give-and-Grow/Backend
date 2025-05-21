from app.models.participant_evaluation import ParticipantEvaluation
from app.extensions import db

def calculate_participant_points(participant_id, db_session):
    total_points = (
        db_session.query(
            db.func.coalesce(db.func.sum(ParticipantEvaluation.score), 0)
        )
        .filter(ParticipantEvaluation.participant_id == participant_id)
        .scalar()
    )
    return total_points