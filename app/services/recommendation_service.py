#Backend/app/services/recommendation_service.py
from flask import request
from app.models.account import Account, Role
from app.models.user_details import UserDetails
from app.models.opportunity import OpportunityType
from app.ml.recommender import recommend_opportunities_for_user
import pandas as pd
from app.ml.collab_data import build_interaction_matrix
from sklearn.metrics.pairwise import cosine_similarity

def compute_user_similarity():
    interaction_matrix = build_interaction_matrix()
    if interaction_matrix is None:
        return None, None, None  

    filled_matrix = interaction_matrix.fillna(0)

    similarity = cosine_similarity(filled_matrix)
    similarity_df = pd.DataFrame(similarity, index=filled_matrix.index, columns=filled_matrix.index)

    return similarity_df, filled_matrix, interaction_matrix     
class RecommendationService:
    @staticmethod
    def get_recommended_opportunities(account_id):
        account = Account.query.get(account_id)
        if not account:
            return {"error": "Account not found"}, 404

        if account.role != Role.USER:
            return {"error": "Unauthorized role"}, 403

        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"error": "User details not found"}, 404

        opportunity_type_param = request.args.get("type", None)
        opportunity_type_enum = None
        if opportunity_type_param:
            opportunity_type_param = opportunity_type_param.lower()
            if opportunity_type_param not in ["volunteer", "job"]:
                return {"error": "Invalid opportunity type"}, 400
            opportunity_type_enum = (
                OpportunityType.VOLUNTEER if opportunity_type_param == "volunteer" else OpportunityType.JOB
            )
        limit = int(request.args.get("limit", 100))
        opportunities = recommend_opportunities_for_user(user_details.id, opportunity_type_enum, limit)
        

        if not opportunities:
            return {"error": "No opportunities found"}, 404

        return opportunities, 200
    
    @staticmethod    
    def recommend_opportunities_for_user_cf(account_id, top_n=5):
        account = Account.query.get(account_id)
        if not account:
            return {"error": "Account not found"}, 404

        if account.role != Role.USER:
            return {"error": "Unauthorized role"}, 403

        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"error": "User details not found"}, 404
        user_id = user_details.id    
        similarity_df, filled_matrix, original_matrix = compute_user_similarity()

        if similarity_df is None or user_id not in similarity_df.index:
            return []

        user_similarities = similarity_df[user_id].drop(labels=[user_id])
        top_users = user_similarities.sort_values(ascending=False).head(5)

        weighted_ratings = pd.Series(dtype='float64')
        for other_user_id, similarity_score in top_users.items():
            other_ratings = filled_matrix.loc[other_user_id]
            weighted = other_ratings * similarity_score
            weighted_ratings = weighted_ratings.add(weighted, fill_value=0)

        user_seen = original_matrix.loc[user_id]
        unseen_opportunities = user_seen[user_seen.isna()].index

        recommendations = weighted_ratings[unseen_opportunities].sort_values(ascending=False).head(top_n)

        return recommendations.index.tolist()

  


    @staticmethod
    def get_similar_users(account_id, top_n=5):
        account = Account.query.get(account_id)
        if not account:
            return {"error": "Account not found"}, 404

        if account.role != Role.USER:
            return {"error": "Unauthorized role"}, 403

        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"error": "User details not found"}, 404
        user_id = user_details.id

        similarity_df, _, _ = compute_user_similarity()

        if similarity_df is None or user_id not in similarity_df.index:
            return []

        user_similarities = similarity_df[user_id].drop(labels=[user_id])
        top_users = user_similarities.sort_values(ascending=False).head(top_n)

        return top_users.to_dict()        
