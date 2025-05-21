from flask import Blueprint, send_file
from PIL import Image, ImageDraw, ImageFont
import os

certificate_bp = Blueprint("certificate", __name__)

def generate_certificate(user_name, from_date, to_date, hours, points, opportunity_title, output_path):
    print("Start generating certificate...")

    # تأكد من وجود صورة الخلفية (شهادة فارغة)
    base_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GreenCertificate.png")
    print(f"Base image path: {base_image_path}")
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f"Background certificate image not found at {base_image_path}")

    image = Image.open(base_image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    # تحديد الخط - لازم يكون عندك ملف خط مناسب في نفس المجلد أو تحدد مسار صحيح
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arial.ttf")
    if not os.path.exists(font_path):
        print("Font file arial.ttf not found, using default font")
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, 24)

    font_large = ImageFont.truetype(font_path, 100)
    font_medium = ImageFont.truetype(font_path, 40)
    font_small = ImageFont.truetype(font_path, 20)

    # كتابة البيانات على الصورة (مثال بسيط)
    draw.text((650, 680), f"{user_name}", fill="black", font=font_large)
    draw.text((700, 940), f" {opportunity_title}", fill="black", font=font_medium)
    draw.text((300, 1130), f"from {from_date} to {to_date}", fill="black", font=font_small)
    draw.text((300, 1220), f"{hours} Hours", fill="black", font=font_small)
    draw.text((300, 1300), f"{points} Points", fill="black", font=font_small)

    image.save(output_path)
    print(f"Certificate saved at {output_path}")

@certificate_bp.route("/download-certificate/<int:opportunity_id>", methods=["GET"])
def download_certificate(opportunity_id):
    print("Start processing /download-certificate route")

    user_name = "Baraa Ahmad"
    from_date = "2025-04-01"
    to_date = "2025-04-15"
    hours = "20"
    points = "50"
    opportunity_title = "Robotics Workshop"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Route base directory: {base_dir}")

    cert_dir = os.path.join(base_dir, "certificates")
    os.makedirs(cert_dir, exist_ok=True)
    print(f"Certificates directory: {cert_dir}")

    cert_filename = f"{user_name.replace(' ', '_')}_{opportunity_id}.pdf"
    cert_path = os.path.join(cert_dir, cert_filename)
    print(f"Certificate file will be saved as: {cert_path}")

    # توليد الشهادة
    generate_certificate(
        user_name=user_name,
        from_date=from_date,
        to_date=to_date,
        hours=hours,
        points=points,
        opportunity_title=opportunity_title,
        output_path=cert_path,
    )

    print(f"Sending file {cert_path}")
    return send_file(cert_path, as_attachment=True)
