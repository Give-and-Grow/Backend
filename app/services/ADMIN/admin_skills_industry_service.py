# Backend/app/services/ADMIN/admin_skills_industry_service.py
from flask import jsonify
from sqlalchemy import func
from app.extensions import db
from app.models import  Skill, opportunity_skills, Opportunity, user_skills, UserDetails
from app.models import Industry, organization_industry, OrganizationDetails


# ========================= SKILLS ========================= #
def create_skill(data):
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    if Skill.query.filter_by(name=name).first():
        return jsonify({"error": "Skill already exists"}), 400

    skill = Skill(name=name)
    db.session.add(skill)
    db.session.commit()
    return jsonify({"message": "Skill created", "skill": {"id": skill.id, "name": skill.name}}), 201


def get_all_skills(search=None, page=1, per_page=10):
    query = Skill.query
    if search:
        query = query.filter(Skill.name.ilike(f"%{search}%"))

    pagination = query.order_by(Skill.name.asc()).paginate(page=page, per_page=per_page, error_out=False)

    skills = [{"id": skill.id, "name": skill.name} for skill in pagination.items]
    return jsonify({
        "skills": skills,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })


def update_skill(skill_id, data):
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found"}), 404

    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    if Skill.query.filter(Skill.name == name, Skill.id != skill_id).first():
        return jsonify({"error": "Skill name already taken"}), 400

    skill.name = name
    db.session.commit()
    return jsonify({"message": "Skill updated", "skill": {"id": skill.id, "name": skill.name}})


def delete_skill(skill_id):
    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Skill not found"}), 404

    db.session.delete(skill)
    db.session.commit()
    return jsonify({"message": "Skill deleted"})


def get_top_used_skills(limit=5):
    result = (
        db.session.query(Skill.name, func.count(opportunity_skills.c.opportunity_id).label("count"))
        .join(opportunity_skills, Skill.id == opportunity_skills.c.skill_id)
        .group_by(Skill.id)
        .order_by(func.count(opportunity_skills.c.opportunity_id).desc())
        .limit(limit)
        .all()
    )

    data = [{"skill": name, "opportunity_count": count} for name, count in result]
    return jsonify({"top_used_skills": data})


def get_user_counts_per_skill():
    result = (
        db.session.query(Skill.name, func.count(user_skills.c.user_id).label("user_count"))
        .join(user_skills, Skill.id == user_skills.c.skill_id)
        .group_by(Skill.id)
        .order_by(func.count(user_skills.c.user_id).desc())
        .all()
    )

    data = [{"skill": name, "user_count": count} for name, count in result]
    return jsonify({"user_counts_per_skill": data})

def get_unused_skills(search=None, page=1, per_page=10):
    query = Skill.query.outerjoin(opportunity_skills).outerjoin(user_skills)
    if search:
        query = query.filter(Skill.name.ilike(f"%{search}%"))

    # Filter skills that are not used in any opportunities or by any users
    query = query.filter(opportunity_skills.c.opportunity_id.is_(None), user_skills.c.user_id.is_(None))

    pagination = query.order_by(Skill.name.asc()).paginate(page=page, per_page=per_page, error_out=False)

    skills = [{"id": skill.id, "name": skill.name} for skill in pagination.items]
    return jsonify({
        "skills": skills,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })

# ========================= INDUSTRIES ========================= #

def create_industry(data):
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    if Industry.query.filter_by(name=name).first():
        return jsonify({"error": "Industry already exists"}), 400

    industry = Industry(name=name)
    db.session.add(industry)
    db.session.commit()
    return jsonify({"message": "Industry created", "industry": {"id": industry.id, "name": industry.name}}), 201


def get_all_industries(search=None, page=1, per_page=10):
    query = Industry.query
    if search:
        query = query.filter(Industry.name.ilike(f"%{search}%"))

    pagination = query.order_by(Industry.name.asc()).paginate(page=page, per_page=per_page, error_out=False)

    industries = [{"id": industry.id, "name": industry.name} for industry in pagination.items]
    return jsonify({
        "industries": industries,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })


def update_industry(industry_id, data):
    industry = Industry.query.get(industry_id)
    if not industry:
        return jsonify({"error": "Industry not found"}), 404

    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    if Industry.query.filter(Industry.name == name, Industry.id != industry_id).first():
        return jsonify({"error": "Industry name already taken"}), 400

    industry.name = name
    db.session.commit()
    return jsonify({"message": "Industry updated", "industry": {"id": industry.id, "name": industry.name}})


def delete_industry(industry_id):
    industry = Industry.query.get(industry_id)
    if not industry:
        return jsonify({"error": "Industry not found"}), 404

    db.session.delete(industry)
    db.session.commit()
    return jsonify({"message": "Industry deleted"})


def get_org_counts_per_industry():
    result = (
        db.session.query(Industry.name, func.count(organization_industry.c.organization_id).label("org_count"))
        .join(organization_industry, Industry.id == organization_industry.c.industry_id)
        .group_by(Industry.id)
        .order_by(func.count(organization_industry.c.organization_id).desc())
        .all()
    )

    data = [{"industry": name, "organization_count": count} for name, count in result]
    return jsonify({"organization_counts_per_industry": data})

def get_unused_industries(search=None, page=1, per_page=10):
    query = Industry.query.outerjoin(organization_industry)
    if search:
        query = query.filter(Industry.name.ilike(f"%{search}%"))

    # Filter industries that are not used by any organizations
    query = query.filter(organization_industry.c.organization_id.is_(None))

    pagination = query.order_by(Industry.name.asc()).paginate(page=page, per_page=per_page, error_out=False)

    industries = [{"id": industry.id, "name": industry.name} for industry in pagination.items]
    return jsonify({
        "industries": industries,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })