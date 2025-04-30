from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.tag import Tag
from app.models.opportunity_tags import opportunity_tags
from app.models.opportunity import Opportunity
from app.models.organization_details import OrganizationDetails
from app.extensions import db
from app.utils.decorators import admin_required, organization_required

tag_bp = Blueprint('tag', __name__)

OFFENSIVE_WORDS = {'fuck', 'shit', 'damn', 'bitch', 'asshole'}



@tag_bp.route('/create', methods=['POST'])
@jwt_required()
def create_tag():
    data = request.get_json()
    name = data.get('name', '').strip().lower()

    if not name:
        return jsonify({"error": "Tag name is required."}), 400

    if name in OFFENSIVE_WORDS:
        return jsonify({"error": "Inappropriate tag name is not allowed."}), 400

    existing = Tag.query.filter_by(name=name).first()
    if existing:
        return jsonify({"message": "Tag already exists.", "tag": {"id": existing.id, "name": existing.name}}), 200

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return jsonify({"message": "Tag created successfully.", "tag": {"id": tag.id, "name": tag.name}}), 201



@tag_bp.route('/<int:tag_id>', methods=['DELETE'])
@admin_required
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found."}), 404

    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "Tag deleted successfully. Offensive tags should not appear to users."}), 200


@tag_bp.route('/assign/<int:opportunity_id>', methods=['POST'])
@organization_required
def assign_tags_to_opportunity(opportunity_id):
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found."}), 404

    current_user_id = get_jwt_identity()
    organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()

    if opportunity.organization_id != organization.id:
        return jsonify({"error": "You do not own this opportunity."}), 403

    data = request.get_json()
    tag_names = data.get('tags', [])

    if not isinstance(tag_names, list) or not all(isinstance(name, str) for name in tag_names):
        return jsonify({"error": "tags must be a list of strings."}), 400

    added_tags = []

    for raw_name in tag_names:
        clean_name = raw_name.strip().lower()

        if not clean_name:
            continue
        if clean_name in OFFENSIVE_WORDS:
            return jsonify({"error": f"The tag '{clean_name}' is not allowed."}), 400

        tag = Tag.query.filter_by(name=clean_name).first()
        if not tag:
            tag = Tag(name=clean_name)
            db.session.add(tag)
            db.session.flush()

        exists = db.session.execute(
            db.select(opportunity_tags).filter_by(opportunity_id=opportunity_id, tag_id=tag.id)
        ).first()

        if not exists:
            stmt = opportunity_tags.insert().values(opportunity_id=opportunity_id, tag_id=tag.id)
            db.session.execute(stmt)
            added_tags.append(tag.name)

    db.session.commit()
    return jsonify({"message": "Tags assigned to opportunity successfully.", "tags_added": added_tags})

@tag_bp.route('/remove/<int:opportunity_id>/<int:tag_id>', methods=['DELETE'])
@organization_required
def remove_tag_from_opportunity(opportunity_id, tag_id):
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found."}), 404

    current_user_id = get_jwt_identity()
    organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()

    if opportunity.organization_id != organization.id:
        return jsonify({"error": "You do not own this opportunity."}), 403

    stmt = opportunity_tags.delete().where(
        opportunity_tags.c.opportunity_id == opportunity_id,
        opportunity_tags.c.tag_id == tag_id
    )
    result = db.session.execute(stmt)
    db.session.commit()

    if result.rowcount == 0:
        return jsonify({"error": "Tag not assigned to this opportunity."}), 404

    return jsonify({"message": "Tag removed from opportunity successfully."})

@tag_bp.route('/', methods=['GET'])
def list_tags():
    query = request.args.get('q', '').strip().lower()
    tags_query = Tag.query
    if query:
        tags_query = tags_query.filter(Tag.name.like(f"%{query}%"))
    tags = tags_query.order_by(Tag.name).all()

    return jsonify([{"id": tag.id, "name": tag.name} for tag in tags])

@tag_bp.route('/opportunity/<int:opportunity_id>', methods=['GET'])
def get_tags_for_opportunity(opportunity_id):
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found."}), 404

    tags = db.session.execute(
        db.select(Tag)
        .join(opportunity_tags, Tag.id == opportunity_tags.c.tag_id)
        .where(opportunity_tags.c.opportunity_id == opportunity_id)
    ).scalars().all()

    return jsonify([{"id": tag.id, "name": tag.name} for tag in tags])
