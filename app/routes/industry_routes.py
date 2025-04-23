#Backend/app/routes/industry_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.industry import Industry
from app.schemas.industry_schema import IndustrySchema
from app.utils.decorators import admin_required

industry_bp = Blueprint("industry", __name__)


@industry_bp.route("/", methods=["GET"])
def list_industries():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    pagination = Industry.query.paginate(page=page, per_page=per_page, error_out=False)
    schema = IndustrySchema(many=True)
    return jsonify({
        "industries": schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200


@industry_bp.route("/", methods=["POST"])
@admin_required
def create_industry():
    data = request.get_json()
    name = data.get("name")

    if Industry.query.filter_by(name=name).first():
        return jsonify({"message": "Industry already exists"}), 400

    industry = Industry(name=name)
    db.session.add(industry)
    db.session.commit()

    return jsonify({
        "message": "Industry created",
        "industry": IndustrySchema().dump(industry)
    }), 201


@industry_bp.route("/<int:industry_id>", methods=["GET"])
def get_industry(industry_id):
    industry = Industry.query.get_or_404(industry_id)
    return jsonify({"industry": IndustrySchema().dump(industry)}), 200


@industry_bp.route("/<int:industry_id>", methods=["PUT"])
@admin_required
def update_industry(industry_id):
    industry = Industry.query.get_or_404(industry_id)
    data = request.get_json()
    industry.name = data.get("name", industry.name)
    db.session.commit()
    return jsonify({
        "message": "Industry updated",
        "industry": IndustrySchema().dump(industry)
    }), 200


@industry_bp.route("/with_counts", methods=["GET"])
@admin_required
def industries_with_counts():
    industries = Industry.query.all()
    result = []
    for industry in industries:
        result.append({
            "id": industry.id,
            "name": industry.name,
            "organization_count": len(industry.organizations)
        })
    return jsonify(result), 200
