from app.models.organization_details import OrganizationDetails 
from app.models.opportunity import Opportunity, OpportunityType
from app.models.volunteer_opportunity import VolunteerOpportunity
from app.models.job_opportunity import JobOpportunity
from app.extensions import db
from sqlalchemy.orm import joinedload
from datetime import datetime
from app.models.account import Account, Role
from marshmallow import ValidationError
from app.schemas.opportunity_schema import OpportunitySchema, FilterOpportunitySchema, OpportunityPaginationSchema,OpportunityGetSchema
from app.models.skill import Skill
from app.models.tag import Tag
from app.utils.unique_opportunity import generate_unique_opportunity_name
from app.utils.location import get_lat_lon_from_location
class OpportunityService:
    @staticmethod
    def create_opportunity(current_user_id,data):
        current_account = Account.query.get(current_user_id)
        if not current_account:
            return {"msg": "Account not found"}, 404

        if current_account.role != Role.ORGANIZATION:
            return {"msg": "Only an organization can create opportunities"}, 403

        organization_details = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if not organization_details:
            return {"msg": "Organization details not found"}, 404   

        # Validate input using OpportunitySchema
        try:
            validated_data = OpportunitySchema().load(data)
        except ValidationError as e:
            return {"msg": "Validation error", "errors": e.messages}, 400

        # Check at least 1 skill is required
        skills = validated_data.get("skills", [])
        if not skills or len(skills) == 0:
            return {"msg": "At least one skill is required"}, 400
        
        location_coords = get_lat_lon_from_location(validated_data.get("location")) if validated_data.get("location") else None

        opportunity = Opportunity(
            organization_id=organization_details.id,
            title=generate_unique_opportunity_name(validated_data["title"]),
            description=validated_data.get("description"),
            location=validated_data.get("location"),
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            status=validated_data.get("status", "open"),
            image_url=validated_data.get("image_url"),
            application_link=validated_data.get("application_link"),
            contact_email=validated_data["contact_email"],
            opportunity_type=validated_data["opportunity_type"],
            latitude=location_coords["latitude"] if location_coords else None,
            longitude=location_coords["longitude"] if location_coords else None,
        )

        db.session.add(opportunity)
        db.session.flush()

        # Link skills
        skills = validated_data.get("skills", [])
        for skill_id in skills:
            skill = Skill.query.get(skill_id)  # استعلام باستخدام ID
            if not skill:
                return {"msg": f"Skill with ID {skill_id} not found"}, 400  # رسالة خطأ إذا لم يوجد المهارة

            opportunity.skills.append(skill)  # ربط المهارة بالفرصة

        # Link tags if available
        tags = validated_data.get("tags", [])
        for tag_id in tags:
            tag = Tag.query.get(tag_id)  # استعلام باستخدام ID
            if not tag:
                return {"msg": f"Tag with ID {tag_id} not found"}, 400  # رسالة خطأ إذا لم يوجد التاج

            opportunity.tags.append(tag)  # ربط التاج بالفرصة

        # Create volunteer or job opportunity details
        if validated_data["opportunity_type"] == "volunteer":
            volunteer_opportunity = VolunteerOpportunity(
                opportunity_id=opportunity.id,
                max_participants=validated_data.get("max_participants"),
                base_points=validated_data.get("base_points", 100),
            )
            db.session.add(volunteer_opportunity)

        elif validated_data["opportunity_type"] == "job":
            job_opportunity = JobOpportunity(
                opportunity_id=opportunity.id,
                required_points=validated_data.get("required_points"),
            )
            db.session.add(job_opportunity)

        db.session.commit()

        return {
            "msg": "Opportunity created successfully",
            "opportunity_id": opportunity.id,
        }, 201

    @staticmethod
    def get_opportunity(opportunity_id):
        opportunity = Opportunity.query.options(
            joinedload(Opportunity.skills),
            joinedload(Opportunity.tags),
            joinedload(Opportunity.volunteer_details),
            joinedload(Opportunity.job_details),
        ).filter_by(id=opportunity_id).first()

        if not opportunity:
            return {"msg": "Opportunity not found"}, 404

        result = OpportunityGetSchema().dump(opportunity)
        return {"opportunity": result}, 200

    @staticmethod
    def list_opportunities(filters):
        query = Opportunity.query.options(
            joinedload(Opportunity.skills),
            joinedload(Opportunity.tags)
        )

        if 'type' in filters:
            query = query.filter(Opportunity.opportunity_type == filters.get('type'))
        if 'status' in filters:
            query = query.filter(Opportunity.status == filters.get('status'))

        page = int(filters.get('page', 1))
        per_page = int(filters.get('per_page', 10))

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        result = OpportunityGetSchema(many=True).dump(pagination.items)
        return {
            "opportunities": result,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200

    # @staticmethod
    # def update_opportunity(current_user_id, opportunity_id, data):
    #     opportunity = Opportunity.query.get(opportunity_id)
    #     if not opportunity:
    #         return {"msg": "Opportunity not found"}, 404

    #     organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
    #     if opportunity.organization_id != organization.id:
    #         return {"msg": "Unauthorized"}, 403

    #     try:
    #         validated_data = OpportunitySchema().load(data, partial=True)
    #     except ValidationError as e:
    #         return {"msg": "Validation error", "errors": e.messages}, 400

    #     for key, value in validated_data.items():
    #         if hasattr(opportunity, key):
    #             setattr(opportunity, key, value)

    #     if "skills" in validated_data:
    #         opportunity.skills.clear()
    #         for skill_id in validated_data["skills"]:
    #             skill = Skill.query.get(skill_id)
    #             if skill:
    #                 opportunity.skills.append(skill)

    #     if "tags" in validated_data:
    #         opportunity.tags.clear()
    #         for tag_id in validated_data["tags"]:
    #             tag = Tag.query.get(tag_id)
    #             if tag:
    #                 opportunity.tags.append(tag)

    #     if opportunity.opportunity_type == OpportunityType.VOLUNTEER:
    #         volunteer = opportunity.volunteer_details
    #         if volunteer:
    #             volunteer.max_participants = validated_data.get("max_participants", volunteer.max_participants)
    #             volunteer.base_points = validated_data.get("base_points", volunteer.base_points)
    #     elif opportunity.opportunity_type == OpportunityType.JOB:
    #         job = opportunity.job_details
    #         if job:
    #             job.required_points = validated_data.get("required_points", job.required_points)

    #     db.session.commit()
    #     return {"msg": "Opportunity updated successfully"}, 200

    # @staticmethod
    # def delete_opportunity(current_user_id, opportunity_id):
    #     opportunity = Opportunity.query.get(opportunity_id)
    #     if not opportunity:
    #         return {"msg": "Opportunity not found"}, 404

    #     organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
    #     if opportunity.organization_id != organization.id:
    #         return {"msg": "Unauthorized"}, 403

    #     db.session.delete(opportunity)
    #     db.session.commit()
    #     return {"msg": "Opportunity deleted successfully"}, 200

    # @staticmethod
    # def change_status(current_user_id, opportunity_id, status):
    #     opportunity = Opportunity.query.get(opportunity_id)
    #     if not opportunity:
    #         return {"msg": "Opportunity not found"}, 404

    #     organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
    #     if opportunity.organization_id != organization.id:
    #         return {"msg": "Unauthorized"}, 403

    #     try:
    #         opportunity.status = OpportunityStatus(status)
    #     except ValueError:
    #         return {"msg": "Invalid status"}, 400

    #     db.session.commit()
    #     return {"msg": "Status updated successfully"}, 200
