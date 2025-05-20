from flask import jsonify
from app.models import  Opportunity, OpportunityParticipant, ParticipantStatus, ParticipantAttendance, ParticipantEvaluation
from datetime import datetime
from app.models.organization_details import OrganizationDetails
from app.extensions import db

def get_opportunity_participants(opportunity_id, org_id):
    organization = OrganizationDetails.query.filter_by(account_id=org_id).first()
    org_id = organization.id if organization else None
    opportunity = Opportunity.query.filter_by(id=opportunity_id, organization_id=org_id).first()
    if not opportunity:
        return jsonify({"error": "Opportunity not found or unauthorized"}), 404

    participants = OpportunityParticipant.query.filter_by(opportunity_id=opportunity_id).all()
    result = [{
        "user_id": p.user_id,
        "status": p.status.value,
        "user_name": p.user.first_name + " " + p.user.last_name,
        "user_profile_image": p.user.profile_picture,
        "applied_at": p.applied_at.isoformat()
    } for p in participants]

    return jsonify(result), 200
def bulk_change_participant_status(opportunity_id, org_account_id, updates):
    organization = OrganizationDetails.query.filter_by(account_id=org_account_id).first()
    if not organization:
        return jsonify({"error": "Unauthorized"}), 403

    opportunity = Opportunity.query.filter_by(id=opportunity_id, organization_id=organization.id).first()
    if not opportunity:
        return jsonify({"error": "Opportunity not found or not owned by this organization"}), 404

    valid_statuses = [status.value for status in ParticipantStatus]
    updated = 0
    skipped = []

    for entry in updates:
        user_id = entry.get("user_id")
        status_value = entry.get("status")

        if not user_id or not status_value:
            skipped.append({"user_id": user_id, "reason": "Missing user_id or status"})
            continue

        if status_value not in valid_statuses:
            skipped.append({"user_id": user_id, "reason": f"Invalid status '{status_value}'"})
            continue

        participant = OpportunityParticipant.query.filter_by(opportunity_id=opportunity_id, user_id=user_id).first()
        if not participant:
            skipped.append({"user_id": user_id, "reason": "Participant not found"})
            continue

        participant.status = ParticipantStatus(status_value)
        updated += 1

    db.session.commit()
    return jsonify({
        "message": f"Status updated for {updated} participants.",
        "skipped": skipped
    }), 200

def change_participant_status(opportunity_id, user_id, org_id, new_status):
    organization = OrganizationDetails.query.filter_by(account_id=org_id).first()
    if not organization:
        return jsonify({"error": "Unauthorized"}), 403

    opportunity = Opportunity.query.filter_by(id=opportunity_id, organization_id=organization.id).first()
    if not opportunity:
        return jsonify({"error": "Opportunity not found or not owned by this organization"}), 404

    participant = OpportunityParticipant.query.filter_by(opportunity_id=opportunity_id, user_id=user_id).first()
    if not participant:
        return jsonify({"error": "Participant not found"}), 404

    try:
        participant.status = ParticipantStatus(new_status)
        db.session.commit()
    except ValueError:
        return jsonify({"error": "Invalid status value"}), 400

    return jsonify({"message": "Participant status updated successfully"}), 200

def fetch_all_applications_for_organization(org_account_id):
    organization = OrganizationDetails.query.filter_by(account_id=org_account_id).first()
    if not organization:
        return jsonify({"error": "Unauthorized"}), 403

    opportunities = Opportunity.query.filter_by(organization_id=organization.id).all()
    opportunity_ids = [op.id for op in opportunities]

    if not opportunity_ids:
        return jsonify([]), 200

    participants = OpportunityParticipant.query.filter(
        OpportunityParticipant.opportunity_id.in_(opportunity_ids)
    ).all()

    result = [{
        "opportunity_id": p.opportunity_id,
        "opportunity_title": p.opportunity.title,
        "user_id": p.user_id,
        "user_name": p.user.first_name + " " + p.user.last_name,
        "user_profile_image": p.user.profile_picture,
        "status": p.status.value,
        "applied_at": p.applied_at.isoformat()
    } for p in participants]

    return jsonify(result), 200
