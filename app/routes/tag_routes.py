from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.tag import Tag
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

@tag_bp.route('/<int:tag_id>', methods=['PUT'])
@admin_required
def update_tag(tag_id):
    data = request.get_json()
    new_name = data.get('name', '').strip().lower()

    if not new_name:
        return jsonify({"error": "New tag name is required."}), 400

    if new_name in OFFENSIVE_WORDS:
        return jsonify({"error": "Inappropriate tag name is not allowed."}), 400

    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found."}), 404

    existing = Tag.query.filter_by(name=new_name).first()
    if existing and existing.id != tag.id:
        return jsonify({"error": "Another tag with this name already exists."}), 400

    tag.name = new_name
    db.session.commit()

    return jsonify({"message": "Tag updated successfully.", "tag": {"id": tag.id, "name": tag.name}})

@tag_bp.route('/suggest', methods=['GET'])
def suggest_tags():
    prefix = request.args.get('q', '').strip().lower()
    if not prefix:
        return jsonify([])

    suggestions = Tag.query.filter(Tag.name.like(f"{prefix}%")).limit(10).all()
    return jsonify([{"id": tag.id, "name": tag.name} for tag in suggestions])


