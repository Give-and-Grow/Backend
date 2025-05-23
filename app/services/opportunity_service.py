#app/services/opportunity_service.py
from app.models.organization_details import OrganizationDetails 
from app.models.opportunity import Opportunity, OpportunityType,OpportunityStatus
from app.models.volunteer_opportunity import VolunteerOpportunity
from app.models.job_opportunity import JobOpportunity
from app.models.opportunity_day import OpportunityDay, WeekDay
from app.extensions import db
from sqlalchemy.orm import joinedload
from datetime import datetime
from app.models.account import Account, Role
from marshmallow import ValidationError
from app.schemas.opportunity_schema import OpportunitySchema
from app.models.skill import Skill
from app.utils.unique_opportunity import generate_unique_opportunity_name
from app.utils.location import get_lat_lon_from_location
from app.utils.distance import haversine_distance
from app.models.user_details import UserDetails  
from sqlalchemy import or_
from datetime import datetime
from app.schemas.opportunity_schema import OpportunityUpdateSchema  
from flask import current_app
import requests
import os
from app.config import Config

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

        try:
            validated_data = OpportunitySchema().load(data)
        except ValidationError as e:
            return {"msg": "Validation error", "errors": e.messages}, 400

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

        skills = validated_data.get("skills", [])
        for skill_id in skills:
            skill = Skill.query.get(skill_id)  
            if not skill:
                return {"msg": f"Skill with ID {skill_id} not found"}, 400  

            opportunity.skills.append(skill)  

         

        if validated_data["opportunity_type"] == "volunteer":
            volunteer_days = validated_data.get("volunteer_days", []) 

            volunteer_opportunity = VolunteerOpportunity(
                opportunity_id=opportunity.id,
                max_participants=validated_data.get("max_participants"),
                base_points=validated_data.get("base_points", 100),
                start_time=validated_data.get("start_time"),
                end_time=validated_data.get("end_time"),
            )
            db.session.add(volunteer_opportunity)
            db.session.flush()  
            for day_str in volunteer_days:
                try:
                    day_enum = WeekDay(day_str.lower())
                except ValueError:
                    return {"msg": f"Invalid day '{day_str}'"}, 400

                opportunity_day = OpportunityDay(
                    volunteer_opportunity_id=volunteer_opportunity.id,
                    day_of_week=day_enum
                )
                db.session.add(opportunity_day)

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
        opportunity = Opportunity.query.filter_by(id=opportunity_id, is_deleted=False).first()

        if not opportunity:
            return {"msg": "Opportunity not found"}, 404

        opportunity_data = {
            "id": opportunity.id,
            "organization_id": opportunity.organization_id,
            "organization_name": opportunity.organization.name if opportunity.organization else None,
            "organization_image": opportunity.organization.logo if opportunity.organization else None,
            "title": opportunity.title,
            "description": opportunity.description,
            "location": opportunity.location,
            "start_date": opportunity.start_date.isoformat() if opportunity.start_date else None,
            "end_date": opportunity.end_date.isoformat() if opportunity.end_date else None,
            "status": opportunity.status.value,
            "image_url": opportunity.image_url,
            "application_link": opportunity.application_link,
            "contact_email": opportunity.contact_email,
            "opportunity_type": opportunity.opportunity_type.value,
            "skills": [{"id": skill.id, "name": skill.name} for skill in opportunity.skills],
        }

        if opportunity.opportunity_type == OpportunityType.VOLUNTEER:
            volunteer = opportunity.volunteer_details
            if volunteer:
                opportunity_data.update({
                    "max_participants": volunteer.max_participants,
                    "base_points": volunteer.base_points,
                    "start_time": volunteer.start_time.strftime("%H:%M") if volunteer.start_time else None,
                    "end_time": volunteer.end_time.strftime("%H:%M") if volunteer.end_time else None,
                    "volunteer_days": [day.day_of_week.value for day in volunteer.days]
                })

        elif opportunity.opportunity_type == OpportunityType.JOB:
            job = opportunity.job_details
            if job:
                opportunity_data["required_points"] = job.required_points

        return {"opportunity": opportunity_data}, 200

    @staticmethod
    def list_opportunities(filters):
        query = Opportunity.query.filter_by(is_deleted=False)

        # --- فلترة حسب الحالة ---
        status = filters.get("status")
        if status:
            try:
                status_enum = OpportunityStatus(status)
                query = query.filter(Opportunity.status == status_enum)
            except ValueError:
                return {"msg": f"Invalid status '{status}'"}, 400

        # --- فلترة حسب النوع ---
        opp_type = filters.get("opportunity_type")
        if opp_type:
            try:
                type_enum = OpportunityType(opp_type)
                query = query.filter(Opportunity.opportunity_type == type_enum)
            except ValueError:
                return {"msg": f"Invalid opportunity type '{opp_type}'"}, 400

        # --- فلترة حسب الموقع ---
        location = filters.get("location")
        if location:
            query = query.filter(Opportunity.location.ilike(f"%{location}%"))

        # --- فلترة حسب التاريخ ---
        start_date = filters.get("start_date")
        if start_date:
            query = query.filter(Opportunity.start_date >= start_date)

        end_date = filters.get("end_date")
        if end_date:
            query = query.filter(Opportunity.end_date <= end_date)

        # --- فلترة حسب المهارة ---
        skill_id = filters.get("skill_id")
        if skill_id and skill_id.isdigit():
            query = query.join(Opportunity.skills).filter_by(id=int(skill_id))

        # --- فلترة حسب المؤسسة ---
        organization_id = filters.get("organization_id")
        if organization_id and organization_id.isdigit():
            query = query.filter(Opportunity.organization_id == int(organization_id))

        # --- فلترة حسب الكلمة المفتاحية ---
        keyword = filters.get("keyword")
        if keyword:
            keyword = f"%{keyword}%"
            query = query.filter(
                db.or_(
                    Opportunity.title.ilike(keyword),
                    Opportunity.description.ilike(keyword)
                )
            )

        # --- فلترة حسب الوقت (لفرص التطوع فقط) ---
        start_time_str = filters.get("start_time")
        end_time_str = filters.get("end_time")
        if start_time_str or end_time_str:
            query = query.join(Opportunity.volunteer_details)
            if start_time_str:
                try:
                    start_time = datetime.strptime(start_time_str, "%H:%M").time()
                    query = query.filter(VolunteerOpportunity.start_time >= start_time)
                except ValueError:
                    return {"msg": "Invalid start_time format. Use HH:MM"}, 400
            if end_time_str:
                try:
                    end_time = datetime.strptime(end_time_str, "%H:%M").time()
                    query = query.filter(VolunteerOpportunity.end_time <= end_time)
                except ValueError:
                    return {"msg": "Invalid end_time format. Use HH:MM"}, 400

        # --- فلترة حسب الأيام (لفرص التطوع فقط) ---
        volunteer_days = filters.get("volunteer_days")
        if volunteer_days:
            day_list = [day.strip().lower() for day in volunteer_days.split(",")]
            try:
                day_enums = [WeekDay(day) for day in day_list]
            except ValueError as e:
                return {"msg": f"Invalid day in volunteer_days: {str(e)}"}, 400

            query = query.join(Opportunity.volunteer_details).join(VolunteerOpportunity.days).filter(
                Opportunity.opportunity_type == OpportunityType.VOLUNTEER,
                OpportunityDay.day_of_week.in_(day_enums)
            )

        # --- ترتيب ---
        sort = filters.get("sort", "newest")
        if sort == "newest":
            query = query.order_by(Opportunity.created_at.desc())
        elif sort == "oldest":
            query = query.order_by(Opportunity.created_at.asc())

        opportunities = query.all()

        results = []
        for opp in opportunities:
            data = {
                "id": opp.id,
                "title": opp.title,
                "description": opp.description,
                "location": opp.location,
                "start_date": opp.start_date.isoformat() if opp.start_date else None,
                "end_date": opp.end_date.isoformat() if opp.end_date else None,
                "status": opp.status.value,
                "image_url": opp.image_url,
                "application_link": opp.application_link,
                "contact_email": opp.contact_email,
                "opportunity_type": opp.opportunity_type.value,
                "organization_id": opp.organization_id,
                "organization_name": opp.organization.name if opp.organization else None,
                "organization_image": opp.organization.logo if opp.organization else None,
                "skills": [{"id": s.id, "name": s.name} for s in opp.skills],
            }

            if opp.opportunity_type == OpportunityType.VOLUNTEER and opp.volunteer_details:
                data["start_time"] = opp.volunteer_details.start_time.strftime("%H:%M") if opp.volunteer_details.start_time else None
                data["end_time"] = opp.volunteer_details.end_time.strftime("%H:%M") if opp.volunteer_details.end_time else None
                data["volunteer_days"] = [d.day_of_week.value for d in opp.volunteer_details.days]

            results.append(data)

        return {"opportunities": results}, 200

    @staticmethod
    def update_opportunity(current_user_id, opportunity_id, data):
        current_account = Account.query.get(current_user_id)
        if not current_account:
            return {"msg": "Account not found"}, 404

        if current_account.role != Role.ORGANIZATION:
            return {"msg": "Only organizations can update opportunities"}, 403

        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity or opportunity.is_deleted:
            return {"msg": "Opportunity not found"}, 404

        organization_details = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if opportunity.organization_id != organization_details.id:
            return {"msg": "You are not authorized to update this opportunity"}, 403

        try:
            validated_data = OpportunityUpdateSchema().load(data)  # ✅ schema المعدل
        except ValidationError as e:
            return {"msg": "Validation error", "errors": e.messages}, 400

        # ✅ تحديث الحقول فقط إذا كانت موجودة
        if "title" in validated_data:
            opportunity.title = generate_unique_opportunity_name(validated_data["title"])
        if "description" in validated_data:
            opportunity.description = validated_data["description"]
        if "location" in validated_data:
            opportunity.location = validated_data["location"]
            location_coords = get_lat_lon_from_location(validated_data["location"])
            opportunity.latitude = location_coords["latitude"] if location_coords else None
            opportunity.longitude = location_coords["longitude"] if location_coords else None
        if "start_date" in validated_data:
            opportunity.start_date = validated_data["start_date"]
        if "end_date" in validated_data:
            opportunity.end_date = validated_data["end_date"]
        if "status" in validated_data:
            opportunity.status = validated_data["status"]
        if "image_url" in validated_data:
            opportunity.image_url = validated_data["image_url"]
        if "application_link" in validated_data:
            opportunity.application_link = validated_data["application_link"]
        if "contact_email" in validated_data:
            opportunity.contact_email = validated_data["contact_email"]

        # ✅ تحديث المهارات إذا انبعثت
        if "skills" in validated_data:
            opportunity.skills.clear()
            for skill_id in validated_data["skills"]:
                skill = Skill.query.get(skill_id)
                if not skill:
                    return {"msg": f"Skill with ID {skill_id} not found"}, 400
                opportunity.skills.append(skill)

        # ✅ حسب نوع الفرصة
        if opportunity.opportunity_type == OpportunityType.VOLUNTEER:
            volunteer_opportunity = opportunity.volunteer_details
            if not volunteer_opportunity:
                return {"msg": "Volunteer opportunity details not found"}, 404

            if "max_participants" in validated_data:
                volunteer_opportunity.max_participants = validated_data["max_participants"]
            if "base_points" in validated_data:
                volunteer_opportunity.base_points = validated_data["base_points"]
            if "start_time" in validated_data:
                volunteer_opportunity.start_time = validated_data["start_time"]
            if "end_time" in validated_data:
                volunteer_opportunity.end_time = validated_data["end_time"]

            if "volunteer_days" in validated_data:
                OpportunityDay.query.filter_by(volunteer_opportunity_id=volunteer_opportunity.id).delete()
                for day in validated_data["volunteer_days"]:
                    new_day = OpportunityDay(
                        volunteer_opportunity_id=volunteer_opportunity.id,
                        day_of_week=day
                    )
                    db.session.add(new_day)

        elif opportunity.opportunity_type == OpportunityType.JOB:
            job = opportunity.job_details
            if not job:
                job = JobOpportunity(opportunity_id=opportunity.id)
                db.session.add(job)
            if "required_points" in validated_data:
                job.required_points = validated_data["required_points"]

        db.session.commit()
        return {"msg": "Opportunity updated successfully"}, 200

    @staticmethod
    def delete_opportunity(current_user_id, opportunity_id):
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {"msg": "Opportunity not found"}, 404

        organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if opportunity.organization_id != organization.id:
            return {"msg": "Unauthorized"}, 403

        opportunity.is_deleted = True
        db.session.commit()

        return {"msg": "Opportunity deleted successfully"}, 200

    @staticmethod
    def restore_opportunity(current_user_id, opportunity_id):
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {"msg": "Opportunity not found"}, 404

        organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if opportunity.organization_id != organization.id:
            return {"msg": "Unauthorized"}, 403

        opportunity.is_deleted = False
        db.session.commit()

        return {"msg": "Opportunity restored successfully"}, 200
    
    @staticmethod
    def get_opportunities_by_organization(current_user_id, filters):
        current_account = Account.query.get(current_user_id)
        if not current_account:
            return {"msg": "Account not found"}, 404

        if current_account.role != Role.ORGANIZATION:
            return {"msg": "Only an organization can create opportunities"}, 403

        organization_details = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if not organization_details:
            return {"msg": "Organization details not found"}, 404 

        filters = dict(filters)
        filters["organization_id"] = str(organization_details.id)  # override any passed organization_id
        return OpportunityService.list_opportunities(filters)

    @staticmethod
    def change_status(current_user_id, opportunity_id, status):
        opportunity = Opportunity.query.get(opportunity_id)
        
        if not opportunity:
            return {"msg": "Opportunity not found"}, 404

        organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if not organization:
            return {"msg": "Organization not found"}, 404
        
        if opportunity.organization_id != organization.id:
            return {"msg": "Unauthorized to modify this opportunity"}, 403

        if opportunity.status.value == status:
            return {"msg": f"Status is already '{status}'"}, 200
        
        try:
            opportunity.status = OpportunityStatus(status)
        except ValueError:
            return {"msg": f"Invalid status: {status}. Valid statuses are {', '.join([s.value for s in OpportunityStatus])}"}, 400

        db.session.commit()
        return {"msg": "Status updated successfully"}, 200

    @staticmethod
    def get_nearby_opportunities(current_user_id, max_distance_km):
        user = UserDetails.query.filter_by(account_id=current_user_id).first()

        user_lat = user.latitude if user and user.latitude is not None else None
        user_lon = user.longitude if user and user.longitude is not None else None

        # جلب كل الفرص النشطة
        all_opps = Opportunity.query.options(
            joinedload(Opportunity.skills),
            joinedload(Opportunity.volunteer_details).joinedload(VolunteerOpportunity.days),
            joinedload(Opportunity.organization)
        ).filter(or_(Opportunity.is_deleted == False, Opportunity.is_deleted == None))

        nearby_opps = []

        if user_lat is not None and user_lon is not None:
            for opp in all_opps:
                if opp.latitude is not None and opp.longitude is not None:
                    distance = haversine_distance(user_lon, user_lat, opp.longitude, opp.latitude)
                    if distance <= max_distance_km:
                        opp_data = OpportunityService.serialize_opportunity(opp)
                        opp_data["distance_km"] = round(distance, 2)
                        nearby_opps.append(opp_data)

        # إذا ما فيه عنوان للمستخدم أو ما طلع فرص قريبة → نجيب فرص الريموت
        if not nearby_opps:
            remote_opps = all_opps.filter(Opportunity.location.ilike("%remote%")).all()

            for opp in remote_opps:
                opp_data = OpportunityService.serialize_opportunity(opp)
                opp_data["distance_km"] = None
                nearby_opps.append(opp_data)

        return {"opportunities": nearby_opps}, 200

    @staticmethod
    def serialize_opportunity(opp):
        data = {
            "id": opp.id,
            "title": opp.title,
            "description": opp.description,
            "location": opp.location,
            "start_date": opp.start_date.isoformat() if opp.start_date else None,
            "end_date": opp.end_date.isoformat() if opp.end_date else None,
            "status": opp.status.value if opp.status else None,
            "image_url": opp.image_url,
            "application_link": opp.application_link,
            "contact_email": opp.contact_email,
            "opportunity_type": opp.opportunity_type.value if opp.opportunity_type else None,
            "organization_id": opp.organization_id,
            "organization_name": opp.organization.name if opp.organization else None,
            "organization_image": opp.organization.logo if opp.organization else None,
            "skills": [{"id": s.id, "name": s.name} for s in opp.skills],
        }

        if opp.opportunity_type == OpportunityType.VOLUNTEER and opp.volunteer_details:
            data["start_time"] = opp.volunteer_details.start_time.strftime("%H:%M") if opp.volunteer_details.start_time else None
            data["end_time"] = opp.volunteer_details.end_time.strftime("%H:%M") if opp.volunteer_details.end_time else None
            data["volunteer_days"] = [d.day_of_week.value for d in opp.volunteer_details.days]

        return data


    @staticmethod
    def generate_ai_summary(opportunity_id):
        from app.models.opportunity import Opportunity
        from sqlalchemy.orm import joinedload
        from app.extensions import db

        opportunity = Opportunity.query.options(
            joinedload(Opportunity.skills),
            joinedload(Opportunity.organization)
        ).filter_by(id=opportunity_id, is_deleted=False).first()

        if not opportunity:
            return "Opportunity not found."

        title = opportunity.title
        description = opportunity.description or "No description provided."
        location = opportunity.location or "No location specified."
        start_date = opportunity.start_date.isoformat() if opportunity.start_date else "N/A"
        end_date = opportunity.end_date.isoformat() if opportunity.end_date else "N/A"
        skills = ", ".join([skill.name for skill in opportunity.skills]) if opportunity.skills else "No specific skills."
        organization_name = opportunity.organization.name if opportunity.organization else "Unknown organization"

        full_text = f"""
        Title: {title}
        Description: {description}
        Location: {location}
        Start Date: {start_date}
        End Date: {end_date}
        Required Skills: {skills}
        Organization: {organization_name}
        """

        try:
            response = requests.post(
                "https://api.apyhub.com/ai/summarize-text",
                headers={
                    "Content-Type": "application/json",
                    "apy-token": os.getenv("APYHUB_API_KEY")  
                },
                json={"text": full_text}
            )
            response.raise_for_status()
            summary = response.json().get("data", "")
            return summary
        except Exception as e:
            return f"Error generating summary: {str(e)}"