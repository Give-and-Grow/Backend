from flask import Blueprint, request, jsonify
from ..extensions import db
from ..services.volunteer_service import  VolunteerService

volunteer_bp = Blueprint("volunteer", __name__, url_prefix="/volunteers")


@volunteer_bp.route("/top/all-honors", methods=["GET"])
def all_honors_volunteers():
    period = request.args.get("period")  # month | smonths | year
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    try:
        data = VolunteerService.get_top_volunteers_all_honors(
            db.session,
            period=period,
            year=year,
            month=month
        )
        return jsonify(data), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Server error: " + str(e)}), 500