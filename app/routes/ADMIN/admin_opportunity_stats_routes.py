#Backend/app/routes/ADMIN/admin_opportunity_stats_routes.py
from flask import Blueprint, request
from app.services.ADMIN.admin_opportunity_stats_service import (
    get_opportunity_counts_by_type,
    get_opportunity_counts_by_status,
    get_top_organizations_by_opportunity_count,
    get_least_active_organizations,
    get_opportunity_count_by_month,
    get_volunteer_opportunity_count_by_weekday,
    get_organization_participation_stats


)

opportunity_stats_bp = Blueprint("opportunity_stats_bp", __name__, url_prefix="/admin/opportunities/stats")

@opportunity_stats_bp.route("/by-type", methods=["GET"])
def opportunity_counts_by_type():
    return get_opportunity_counts_by_type()

@opportunity_stats_bp.route("/by-status", methods=["GET"])
def opportunity_counts_by_status():
    return get_opportunity_counts_by_status()


@opportunity_stats_bp.route("/top-organizations", methods=["GET"])
def top_organizations_by_opportunities():
    limit = int(request.args.get("limit", 5))
    return get_top_organizations_by_opportunity_count(limit)

@opportunity_stats_bp.route("/least-active-organizations", methods=["GET"])
def least_active_organizations():
    limit = int(request.args.get("limit", 5))
    return get_least_active_organizations(limit)

@opportunity_stats_bp.route("/by-month", methods=["GET"])
def opportunities_by_month_route():
    return get_opportunity_count_by_month()

@opportunity_stats_bp.route("/by-day", methods=["GET"])
def opportunities_by_day_route():
    return get_volunteer_opportunity_count_by_weekday()


@opportunity_stats_bp.route("/top-organizations-by-participation", methods=["GET"])
def top_organizations_by_participation():
    return get_organization_participation_stats()
