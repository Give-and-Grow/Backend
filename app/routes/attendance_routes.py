from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.participant_attendance import ParticipantAttendance, AttendanceStatus
from app.extensions import db
from datetime import datetime
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app.models.opportunity import Opportunity
from app.models.opportunity_day import OpportunityDay, WeekDay
from app.models.opportunity_participant import OpportunityParticipant



attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")


@attendance_bp.route("/<int:opportunity_id>/dates", methods=["GET"])
def get_attendance_dates(opportunity_id):
    opportunity = Opportunity.query.filter_by(id=opportunity_id, is_deleted=False).first()
    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    opportunity_days = OpportunityDay.query.filter_by(volunteer_opportunity_id=opportunity.volunteer_details.id).all()
    days_of_week = set(day.day_of_week.value for day in opportunity_days)

    start_date = opportunity.start_date
    end_date = opportunity.end_date

    if not start_date or not end_date:
        return jsonify({"error": "Opportunity dates are not set"}), 400

    current_date = start_date
    valid_dates = []
    while current_date <= end_date:
        if current_date.strftime("%A").lower() in days_of_week:
            valid_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return jsonify({"dates": valid_dates}), 200

from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.models.participant_attendance import ParticipantAttendance, AttendanceStatus
from flask_jwt_extended import jwt_required

@attendance_bp.route("/<int:opportunity_id>", methods=["GET"])
@jwt_required()
def get_participants_attendance(opportunity_id):
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"error": "Missing date parameter"}), 400

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    opportunity = Opportunity.query.filter_by(id=opportunity_id, is_deleted=False).first()
    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    participants = OpportunityParticipant.query.filter_by(
        opportunity_id=opportunity_id,
        status=ParticipantStatus.ACCEPTED
    ).all()

    response = []
    for p in participants:
        attendance_record = ParticipantAttendance.query.filter_by(
            participant_id=p.id,
            date=date
        ).first()

        status = attendance_record.status.value if attendance_record else "present"  

        response.append({
            "participant_id": p.id,
            "name": p.user.first_name + " " + p.user.last_name,
            "profile_picture": p.user.profile_picture,
            "phone": p.user.phone_number,
            "user_id": p.user_id,
            "status": status
        })

    return jsonify({"date": date_str, "participants": response}), 200

@attendance_bp.route("/<int:opportunity_id>", methods=["POST"])
@jwt_required()
def post_attendance(opportunity_id):
    try:
        # Get request data
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input: Expected a list of attendance records"}), 400
            
        # Validate required fields for each attendance record
        required_fields = ["participant_id", "date", "status"]
        valid_statuses = [status.value for status in AttendanceStatus]
        
        for record in data:
            # Check for required fields
            if not all(field in record for field in required_fields):
                return jsonify({"error": f"Missing required fields: {required_fields}"}), 400
                
            # Validate participant_id
            participant = OpportunityParticipant.query.filter_by(
                id=record["participant_id"],
                opportunity_id=opportunity_id
            ).first()
            if not participant:
                return jsonify({"error": f"Participant {record['participant_id']} not found for this opportunity"}), 404
                
            # Validate date format
            try:
                attendance_date = datetime.strptime(record["date"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": f"Invalid date format for participant {record['participant_id']}: Use YYYY-MM-DD"}), 400
                
            # Normalize and validate status
            status = record["status"].lower()  # Convert to lowercase
            if status not in valid_statuses:
                return jsonify({"error": f"Invalid status for participant {record['participant_id']}: Must be one of {valid_statuses}"}), 400
                
            # Check if attendance record already exists
            existing_record = ParticipantAttendance.query.filter_by(
                participant_id=record["participant_id"],
                date=attendance_date
            ).first()
            if existing_record:
                # Update existing record
                existing_record.status = AttendanceStatus(status)
            else:
                # Create new attendance record
                new_attendance = ParticipantAttendance(
                    participant_id=record["participant_id"],
                    date=attendance_date,
                    status=AttendanceStatus(status)
                )
                db.session.add(new_attendance)
                print(new_attendance.status)
                print(new_attendance.participant_id)
        
        # Commit all changes
        db.session.commit()
        
        return jsonify({
            "message": "Attendance records processed successfully",
            "count": len(data)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500