# Backend/app/routes/ADMIN/admin_skills_industry_routes.py
from flask import Blueprint, request, jsonify
from app.services.ADMIN.admin_skills_industry_service import *


skills_admin_bp = Blueprint("skills_admin_bp", __name__, url_prefix="/admin/skills")
industry_admin_bp = Blueprint("industry_admin_bp", __name__, url_prefix="/admin/industries")

# ========================= SKILLS ========================= #
@skills_admin_bp.route("/", methods=["POST"])
def create_skill_route():
    data = request.json
    return create_skill(data)

@skills_admin_bp.route("/", methods=["GET"])
def get_all_skills_route():
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    return get_all_skills(search, page, per_page)

@skills_admin_bp.route("/<int:skill_id>", methods=["PUT"])
def update_skill_route(skill_id):
    data = request.json
    return update_skill(skill_id, data)

@skills_admin_bp.route("/<int:skill_id>", methods=["DELETE"])
def delete_skill_route(skill_id):
    return delete_skill(skill_id)

@skills_admin_bp.route("/top-used", methods=["GET"])
def top_used_skills_route():
    limit = int(request.args.get("limit", 5))
    return get_top_used_skills(limit)

@skills_admin_bp.route("/user-counts", methods=["GET"])
def user_counts_per_skill_route():
    return get_user_counts_per_skill()
#skills with no usage
@skills_admin_bp.route("/unused", methods=["GET"])
def unused_skills_route():
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    return get_unused_skills(search, page, per_page)    

# ========================= INDUSTRIES ========================= #
@industry_admin_bp.route("/", methods=["POST"])
def create_industry_route():
    data = request.json
    return create_industry(data)

@industry_admin_bp.route("/", methods=["GET"])
def get_all_industries_route():
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    return get_all_industries(search, page, per_page)

@industry_admin_bp.route("/<int:industry_id>", methods=["PUT"])
def update_industry_route(industry_id):
    data = request.json
    return update_industry(industry_id, data)

@industry_admin_bp.route("/<int:industry_id>", methods=["DELETE"])
def delete_industry_route(industry_id):
    return delete_industry(industry_id)

@industry_admin_bp.route("/org-counts", methods=["GET"])
def org_counts_per_industry_route():
    return get_org_counts_per_industry()

@industry_admin_bp.route("/unused", methods=["GET"])
def unused_industries_route():
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    return get_unused_industries(search, page, per_page)
