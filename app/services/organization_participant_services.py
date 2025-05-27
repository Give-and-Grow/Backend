from flask import jsonify
from app.models import  Opportunity, OpportunityParticipant, ParticipantStatus, ParticipantAttendance, ParticipantEvaluation
from datetime import datetime
from app.models.organization_details import OrganizationDetails
from app.extensions import db
from app.services.notification_service import notify_user

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

    
    status_titles = {
        "accepted": "You have been accepted!",
        "rejected": "Your application was rejected",
        "pending": "Your application is under review",
        "cancelled": "Your participation has been cancelled"
      
    }

    status_bodies = {
        "accepted": f"You have been accepted for the opportunity '{opportunity.title}' by {organization.name}.",
        "rejected": f"Unfortunately, you were not selected for the opportunity '{opportunity.title}'.",
        "pending": f"Your request to join the opportunity '{opportunity.title}' is under review.",
        "cancelled": f"Your participation in the opportunity '{opportunity.title}' has been cancelled."
       
    }

    if new_status in status_titles:
        notify_user(
            user_id=user_id,
            title=status_titles[new_status],
            body=status_bodies[new_status],
            data={
                "type": "opportunity_status",
                "opportunity_id": opportunity.id,
                "status": new_status,
                "from": org_id  
            }
        )

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
