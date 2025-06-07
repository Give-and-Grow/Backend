from app import create_app
from app.extensions import db
from app.models.account import Account, Role
from app.models.organization_details import OrganizationDetails, VerificationStatus
from app.models.industry import Industry

app = create_app()

# List of industries to populate
industries = [
    "Healthcare",
    "Education",
    "Human Rights",
    "Community Development",
    "Environmental Sustainability",
    "Agriculture",
    "Youth Empowerment",
    "Women's Empowerment",
    "Peacebuilding",
    "Economic Development",
    "Cultural Preservation"
]

organizations = [
    {
        "name": "Palestine Red Crescent Society",
        "email": "info@palestinercs.org",
        "description": "A national humanitarian organization providing healthcare and welfare services to Palestinians.",
        "phone": "+970 2 240 6515",
        "address": "Ramallah, Palestine",
        "industries": ["Healthcare", "Community Development"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Taawon",
        "email": "contact@taawon.org",
        "description": "The largest Palestinian non-profit supporting education, culture, and community development.",
        "phone": "+970 2 294 3170",
        "address": "Ramallah, Palestine",
        "industries": ["Education", "Community Development", "Cultural Preservation"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Medical Aid for Palestinians (MAP)",
        "email": "info@map.org.uk",
        "description": "Delivers medical aid and develops healthcare systems for Palestinians under occupation.",
        "phone": "+970 2 240 1177",
        "address": "Gaza, Palestine",
        "industries": ["Healthcare"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Applied Research Institute-Jerusalem (ARIJ)",
        "email": "info@arij.org",
        "description": "Focuses on environmental, water, agriculture, and good governance research.",
        "phone": "+970 2 274 1889",
        "address": "Bethlehem, Palestine",
        "industries": ["Environmental Sustainability", "Agriculture"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "MIFTAH",
        "email": "info@miftah.org",
        "description": "Promotes democracy, public debate, and Palestinian nation-building.",
        "phone": "+970 2 298 9490",
        "address": "Ramallah, Palestine",
        "industries": ["Human Rights", "Peacebuilding"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Al-Haq",
        "email": "info@alhaq.org",
        "description": "A human rights organization documenting violations in the Occupied Palestinian Territories.",
        "phone": "+970 2 295 4646",
        "address": "Ramallah, Palestine",
        "industries": ["Human Rights"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Palestinian Center for Rapprochement (PCR)",
        "email": "info@pcr.ps",
        "description": "Promotes media, community service, youth empowerment, and international solidarity.",
        "phone": "+970 2 277 2018",
        "address": "Beit Sahour, Palestine",
        "industries": ["Community Development", "Youth Empowerment"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Diyar Consortium",
        "email": "info@diyar.ps",
        "description": "Focuses on community development, elderly care, and health programs.",
        "phone": "+970 2 277 0047",
        "address": "Bethlehem, Palestine",
        "industries": ["Community Development", "Healthcare"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Middle East Nonviolence and Democracy (MEND)",
        "email": "info@mendonline.org",
        "description": "Provides nonviolence training and empowerment programs for youth and women.",
        "phone": "+970 2 297 1382",
        "address": "Ramallah, Palestine",
        "industries": ["Youth Empowerment", "Women's Empowerment", "Peacebuilding"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Water and Environmental Development Organization (WEDO)",
        "email": "info@wedo-pal.org",
        "description": "Promotes environmental protection and ecotourism in Palestine.",
        "phone": "+970 2 275 0570",
        "address": "Jericho, Palestine",
        "industries": ["Environmental Sustainability"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Palestinian American Medical Association (PAMA)",
        "email": "info@pamausa.org",
        "description": "Promotes healthcare and medical education for Palestinians.",
        "phone": "+970 2 295 1234",
        "address": "Ramallah, Palestine",
        "industries": ["Healthcare", "Education"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "ADDAMEER",
        "email": "info@addameer.org",
        "description": "Supports Palestinian prisoners and advocates for their rights.",
        "phone": "+970 2 296 0446",
        "address": "Ramallah, Palestine",
        "industries": ["Human Rights"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Al-Shabaka",
        "email": "info@al-shabaka.org",
        "description": "A think tank fostering public debate on Palestinian human rights and self-determination.",
        "phone": "+970 2 298 1234",
        "address": "Ramallah, Palestine",
        "industries": ["Human Rights"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "HEAL Palestine",
        "email": "info@healpalestine.org",
        "description": "Focuses on health, education, and leadership development for Palestinian youth.",
        "phone": "+970 2 241 2345",
        "address": "Gaza, Palestine",
        "industries": ["Healthcare", "Education", "Youth Empowerment"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Palestinian Conflict Resolution Center (WI’AM)",
        "email": "info@wiam.ps",
        "description": "Promotes mediation, non-violence training, and community empowerment.",
        "phone": "+970 2 277 0513",
        "address": "Bethlehem, Palestine",
        "industries": ["Peacebuilding", "Community Development"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Palestinian Federation of Industries (PFI)",
        "email": "info@pfi.ps",
        "description": "Represents and supports the Palestinian industrial sector.",
        "phone": "+970 2 295 5678",
        "address": "Ramallah, Palestine",
        "industries": ["Economic Development"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Hakini",
        "email": "info@hakini.ps",
        "description": "Provides mental health services and psychological support in Palestine.",
        "phone": "+970 2 240 9876",
        "address": "Gaza, Palestine",
        "industries": ["Healthcare"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "United Palestinian Appeal (UPA)",
        "email": "info@upaconnect.org",
        "description": "Supports socio-economic and cultural development for Palestinians.",
        "phone": "+970 2 298 7654",
        "address": "Ramallah, Palestine",
        "industries": ["Community Development", "Cultural Preservation"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Palestine Boycott, Divestment and Sanctions National Committee (BNC)",
        "email": "info@bdsmovement.net",
        "description": "A coalition advocating for the BDS movement to support Palestinian rights.",
        "phone": "+970 2 297 2345",
        "address": "Ramallah, Palestine",
        "industries": ["Human Rights"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
    {
        "name": "Palestinian Academic Society for the Study of International Affairs (PASSIA)",
        "email": "info@passia.org",
        "description": "Conducts research on Palestinian issues in national and international contexts.",
        "phone": "+970 2 626 4426",
        "address": "Jerusalem, Palestine",
        "industries": ["Education", "Human Rights"],
        "proof_image": "proof.jpg",
        "proof_verification_status": "APPROVED"
    },
]
new_fcm_token = 'fo_b6ICPfYytDj4WfGvi11:APA91bEcXiizkv7gH_SMIFaNlz0L3oqLxqq49mzO_k-OWI0ijvjPmyKuCO5-kINhFk7HTBhl5dmDBBLmnMd8hUITBYErRBWg6zESL6mLQY-FjLE8Sa2Wg8A'

def seed_industries():
    """Populate the industry table with required industries."""
    with app.app_context():
        for industry_name in industries:
            industry = Industry.query.filter_by(name=industry_name).first()
            if not industry:
                industry = Industry(name=industry_name)
                db.session.add(industry)
        db.session.commit()
        print(f"✅ تم إدخال {len(industries)} صناعات بنجاح.")

def seed_organizations():
    with app.app_context():
        # جلب كل الصناعات الموجودة في قاعدة البيانات كقاموس: اسم -> كائن Industry
        industry_map = {ind.name: ind for ind in Industry.query.all()}

        for org in organizations:
            # التحقق من وجود الحساب مسبقًا
            account = Account.query.filter_by(email=org["email"]).first()
            if not account:
                # إنشاء اسم مستخدم فريد بناءً على اسم المؤسسة
                name_parts = org["name"].split()
                base_username = "_".join(name_parts[:2]).lower()
                username = base_username 
                # التأكد من أن اسم المستخدم فريد
                existing_usernames = {a.username for a in Account.query.all()}
                i = 1
                if username in existing_usernames:
                    if len(name_parts) >= 3:
                        username = "_".join(name_parts[:3]).lower()
                    while username in existing_usernames:
                        username = f"{base_username}_{i}"
                        i += 1

                account = Account(
                    email=org["email"],
                    username=username,
                    role=Role.ORGANIZATION,
                    is_email_verified=True,
                    is_active=True,
                    fcm_token=new_fcm_token
                )
                account.set_password("Orga123!")  # كلمة السر الثابتة
                db.session.add(account)

            # التحقق من وجود تفاصيل المؤسسة مسبقًا
            org_details = OrganizationDetails.query.filter_by(account_id=account.id).first()
            if not org_details:
                org_details = OrganizationDetails(
                    account=account,
                    name=org["name"],
                    description=org["description"],
                    phone=org["phone"],
                    address=org["address"],
                    proof_image=org["proof_image"],
                    proof_verification_status=VerificationStatus[org["proof_verification_status"]],
                    is_active=True,
                    logo=f"https://ui-avatars.com/api/?name={org['name'].replace(' ', '+')}&background=random",
                )
                db.session.add(org_details)

            # ربط الصناعات
            for industry_name in org["industries"]:
                industry = industry_map.get(industry_name)
                if industry and industry not in org_details.industries:
                    org_details.industries.append(industry)
                elif not industry:
                    print(f"⚠️ Industry '{industry_name}' not found for organization '{org['name']}'")

        db.session.commit()
        print(f"✅ {len(organizations)} ")

if __name__ == "__main__":
    seed_industries()  
    seed_organizations()  