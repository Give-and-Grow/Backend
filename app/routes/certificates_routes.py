from flask import Blueprint, send_file
from PIL import Image, ImageDraw, ImageFont
from flask_jwt_extended import jwt_required
from app.models.user_details import UserDetails
from flask_jwt_extended import get_jwt_identity, get_jwt
import os
from app.utils.calculate_hours import calculate_volunteer_hours 
from app.models.opportunity import Opportunity  
from app.extensions import db
from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.utils.calculate_points import calculate_participant_points
from decimal import Decimal
from io import BytesIO

certificate_bp = Blueprint("certificate", __name__)



def generate_certificate(user_name, from_date, to_date, hours, points, opportunity_title):
    base_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GreenCertificate.png")

    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f"Background certificate image not found at {base_image_path}")

    image = Image.open(base_image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arial.ttf")
    if not os.path.exists(font_path):
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, 24)

    font_large = ImageFont.truetype(font_path, 100)
    font_medium = ImageFont.truetype(font_path, 50)
    font_small = ImageFont.truetype(font_path, 30)

    draw.text((650, 680), f"{user_name}", fill="black", font=font_large)
    draw.text((700, 940), f"{opportunity_title}", fill="black", font=font_medium)
    draw.text((300, 1130), f"from {from_date} to {to_date}", fill="black", font=font_small)
    draw.text((300, 1220), f"{hours} Hours", fill="black", font=font_small)
    draw.text((300, 1300), f"{points} Points", fill="black", font=font_small)

    # حفظ الصورة في BytesIO بدلاً من ملف فعلي
    output_bytes = BytesIO()
    image.save(output_bytes, format="PDF")
    output_bytes.seek(0)
    return output_bytes


@certificate_bp.route("/download-certificate/<int:opportunity_id>", methods=["GET"])
@jwt_required()
def download_certificate(opportunity_id):
    current_user_id = get_jwt_identity() 
    claims = get_jwt()
    if claims["role"] != "user":
        return {"msg": "You are not authorized to access this route"}, 403

    user = UserDetails.query.filter_by(account_id=current_user_id).first()
    if not user:
        return {"msg": "User not found"}, 404

    participant = OpportunityParticipant.query.filter_by(
        user_id=user.id,
        opportunity_id=opportunity_id
    ).first()
    if not participant:
        return {"msg": "You are not a participant in this opportunity"}, 404        

    opportunity = Opportunity.query.filter_by(id=opportunity_id).first()
    if not opportunity:
        return {"msg": "Opportunity not found"}, 404    

    result = calculate_volunteer_hours(opportunity, user.id, db.session)
    if not result:
        return {"msg": "No hours calculated"}, 404

    user_name = user.first_name + " " + user.last_name
    from_date = opportunity.start_date.strftime("%Y-%m-%d")
    to_date = opportunity.end_date.strftime("%Y-%m-%d")
    hours = round(result["attended_hours"], 1)
    points = int(calculate_participant_points(participant.id, db.session) * Decimal(str(hours)))
    opportunity_title = opportunity.title

    # توليد الشهادة كـ BytesIO
    pdf_bytes = generate_certificate(
        user_name=user_name,
        from_date=from_date,
        to_date=to_date,
        hours=hours,
        points=points,
        opportunity_title=opportunity_title,
    )

    cert_filename = f"{user_name.replace(' ', '_')}_{opportunity_id}.pdf"

    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name=cert_filename,
        mimetype='application/pdf'
    )
