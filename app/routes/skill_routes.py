# Backend/app/routes/skill_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.skill import Skill
from app.models.opportunity_skills import opportunity_skills
from app.models.opportunity import Opportunity
from app.extensions import db
from app.utils.decorators import admin_required, organization_required
from flask_jwt_extended import get_jwt_identity
from app.models.organization_details import OrganizationDetails 

skill_bp = Blueprint('skill', __name__)



@skill_bp.route('/', methods=['POST'])
@admin_required
def create_skill():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Skill name is required"}), 400

    if Skill.query.filter_by(name=name).first():
        return jsonify({"error": "Skill already exists"}), 400

    skill = Skill(name=name)
    db.session.add(skill)
    db.session.commit()

    return jsonify({"message": "Skill created successfully.", "skill": {"id": skill.id, "name": skill.name}}), 201


@skill_bp.route('/<int:skill_id>', methods=['PUT'])
@admin_required
def update_skill(skill_id):
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Skill name is required"}), 400

    skill.name = name
    db.session.commit()

    return jsonify({"message": "Skill updated successfully.", "skill": {"id": skill.id, "name": skill.name}})


@skill_bp.route('/<int:skill_id>', methods=['DELETE'])
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found."}), 404

    db.session.delete(skill)
    db.session.commit()

    return jsonify({"message": "Skill deleted successfully."})


@skill_bp.route('/assign/<int:opportunity_id>', methods=['POST'])
@organization_required
def assign_skills_to_opportunity(opportunity_id):
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found."}), 404

    
    current_user_id = get_jwt_identity()
    organization_details = OrganizationDetails.query.filter_by(account_id=current_user_id).first()  
    if opportunity.organization_id != organization_details.id:
        return jsonify({"error": "You do not own this opportunity."}), 403

    data = request.get_json()
    skill_ids = data.get('skill_ids')

    if not isinstance(skill_ids, list) or not all(isinstance(id, int) for id in skill_ids):
        return jsonify({"error": "skill_ids must be a list of integers."}), 400

    for skill_id in skill_ids:
        skill = Skill.query.get(skill_id)
        if not skill:
            return jsonify({"error": f"Skill with id {skill_id} not found."}), 404

        exists = db.session.execute(
            db.select(opportunity_skills)
            .filter_by(opportunity_id=opportunity_id, skill_id=skill_id)
        ).first()

        if not exists:
            stmt = opportunity_skills.insert().values(opportunity_id=opportunity_id, skill_id=skill_id)
            db.session.execute(stmt)

    db.session.commit()

    return jsonify({"message": "Skills assigned to opportunity successfully."})


@skill_bp.route('/remove/<int:opportunity_id>/<int:skill_id>', methods=['DELETE'])
@organization_required
def remove_skill_from_opportunity(opportunity_id, skill_id):
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found."}), 404

    from flask_jwt_extended import get_jwt_identity
    current_user_id = get_jwt_identity()

    current_user_id = get_jwt_identity()
    organization_details = OrganizationDetails.query.filter_by(account_id=current_user_id).first()  
    if opportunity.organization_id != organization_details.id:
        return jsonify({"error": "You do not own this opportunity."}), 403

    stmt = opportunity_skills.delete().where(
        opportunity_skills.c.opportunity_id == opportunity_id,
        opportunity_skills.c.skill_id == skill_id
    )
    result = db.session.execute(stmt)
    db.session.commit()

    if result.rowcount == 0:
        return jsonify({"error": "Skill not assigned to this opportunity."}), 404

    return jsonify({"message": "Skill removed from opportunity successfully."})



@skill_bp.route('/', methods=['GET'])
def list_skills():
    skills = Skill.query.all()
    return jsonify([
        {"id": skill.id, "name": skill.name}
        for skill in skills
    ])


@skill_bp.route('/opportunity/<int:opportunity_id>', methods=['GET'])
def get_skills_for_opportunity(opportunity_id):
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found."}), 404

    skills = db.session.execute(
        db.select(Skill)
        .join(opportunity_skills, Skill.id == opportunity_skills.c.skill_id)
        .where(opportunity_skills.c.opportunity_id == opportunity_id)
    ).scalars().all()

    return jsonify([
        {"id": skill.id, "name": skill.name}
        for skill in skills
    ])
