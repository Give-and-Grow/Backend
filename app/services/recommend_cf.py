from app.extensions import db
from app.models import ParticipantEvaluation, OpportunityParticipant, Opportunity
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def build_rating_matrix():
    # جلب البيانات: org_id, user_id, score
    query = db.session.query(
        Opportunity.id.label("opportunity_id"),
        Opportunity.organization_id.label("org_id"),
        OpportunityParticipant.user_id.label("user_id"),
        ParticipantEvaluation.score.label("score")
    ).join(OpportunityParticipant, ParticipantEvaluation.participant_id == OpportunityParticipant.id
    ).join(Opportunity, OpportunityParticipant.opportunity_id == Opportunity.id)

    df = pd.read_sql(query.statement, db.session.bind)

    # pivot table: مؤسسة × متطوع
    rating_matrix = df.pivot_table(index="org_id", columns="user_id", values="score").fillna(0)

    return rating_matrix


def recommend_users_for_org(org_id: int, top_n: int = 5):
    rating_matrix = build_rating_matrix()

    if org_id not in rating_matrix.index:
        return []

    similarity = cosine_similarity(rating_matrix)
    similarity_df = pd.DataFrame(similarity, index=rating_matrix.index, columns=rating_matrix.index)

    org_sim = similarity_df[org_id].drop(org_id)  # drop self
    weighted_scores = rating_matrix.T.dot(org_sim)

    # المتطوعين الذين لم تقيّمهم المؤسسة الحالية
    rated_by_org = rating_matrix.loc[org_id]
    unrated_users = rated_by_org[rated_by_org == 0].index

    suggestions = weighted_scores[unrated_users].sort_values(ascending=False)
    recommended_user_ids = list(suggestions.head(top_n).index)

    return recommended_user_ids
from app.utils.email import send_invitation_email
from app.models import UserDetails, Opportunity, OrganizationDetails

def invite_recommended_users(opportunity_id, user_ids):
    opportunity = Opportunity.query.get(opportunity_id)
    organization = OrganizationDetails.query.get(opportunity.org_id)

    link = f"https://givandgrow.com/opportunity/{opportunity_id}"  # أو حسب موقعك الفعلي

    for user_id in user_ids:
        user = UserDetails.query.get(user_id)
        if user and user.email:
            send_invitation_email(
                user_email=user.email,
                opportunity_title=opportunity.title,
                organization_name=organization.name,
                join_link=link
            )