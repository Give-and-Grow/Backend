from flask import Blueprint, request, jsonify
from app.services.opportunity_service import OpportunityService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import organization_required
from app.utils.distance import haversine_distance
from app.models.opportunity import Opportunity
from app.models.user_details import UserDetails  
from app.extensions import db

opportunity_bp = Blueprint('opportunity_bp', __name__)

@opportunity_bp.route('/create', methods=['POST'])
@jwt_required()
def create_opportunity():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    return OpportunityService.create_opportunity(current_user_id,data)
    
@opportunity_bp.route('/<int:opportunity_id>', methods=['GET'])
def get_opportunity(opportunity_id):
    return OpportunityService.get_opportunity(opportunity_id)

@opportunity_bp.route('/list', methods=['GET'])
def list_opportunities():
    filters = request.args  # يمكنك تمرير فلترة بالـ query string
    return OpportunityService.list_opportunities(filters)

@opportunity_bp.route('/<int:opportunity_id>', methods=['PUT'])
@jwt_required()
def update_opportunity(opportunity_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    return OpportunityService.update_opportunity(current_user_id, opportunity_id, data)

@opportunity_bp.route('/<int:opportunity_id>', methods=['DELETE'])
@jwt_required()
def delete_opportunity(opportunity_id):
    current_user_id = get_jwt_identity()
    return OpportunityService.delete_opportunity(current_user_id, opportunity_id)

@opportunity_bp.route('/organization', methods=['GET'])
@jwt_required()
def get_opportunities_by_organization():
    current_user_id = get_jwt_identity()
    filters = request.args  # أو استخدم request.get_json() لو كانت البيانات JSON

    return OpportunityService.get_opportunities_by_organization(current_user_id, filters)


@opportunity_bp.route('/<int:opportunity_id>/change-status', methods=['PATCH'])
@jwt_required()
def change_status(opportunity_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # التأكد من وجود "status" في البيانات
    status = data.get('status')
    if not status:
        return {"msg": "Missing 'status' in request data"}, 400
    
    # استدعاء خدمة تغيير الحالة
    return OpportunityService.change_status(current_user_id, opportunity_id, status)


# @opportunity_bp.route("/nearby_opportunities", methods=["GET"])
# @jwt_required()  # تأكد من وجود هذا الديكوريتر!
# def get_nearby_opportunities():
#     current_user_id = get_jwt_identity()  # هذا يرجع account_id

#     max_distance_km = float(request.args.get("max_distance", 50))

#     user = UserDetails.query.filter_by(account_id=current_user_id).first()
#     if not user or user.latitude is None or user.longitude is None:
#         return jsonify({"msg": "User location not found"}), 404

#     user_lat = user.latitude
#     user_lon = user.longitude

#     all_opps = Opportunity.query.all()
#     nearby_opps = []

#     for opp in all_opps:
#         if opp.latitude is not None and opp.longitude is not None:
#             distance = haversine_distance(user_lon, user_lat, opp.longitude, opp.latitude)
#             if distance <= max_distance_km:
#                 opp_data = {
#                     "id": opp.id,
#                     "title": opp.title,
#                     "description": opp.description,
#                     "distance_km": round(distance, 2),
#                 }
#                 nearby_opps.append(opp_data)

#     return jsonify({"opportunities": nearby_opps}), 200

@opportunity_bp.route("/nearby_opportunities", methods=["GET"])
@jwt_required()
def get_nearby_opportunities():
    current_user_id = get_jwt_identity()
    max_distance_km = float(request.args.get("max_distance", 50))  
    return OpportunityService.get_nearby_opportunities(current_user_id, max_distance_km)
