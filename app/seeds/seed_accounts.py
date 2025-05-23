# Backend/app/seeds/seed_accounts.py

import os
from dotenv import load_dotenv
import mysql.connector
import logging
from faker import Faker  
import random
from datetime import datetime, timedelta

from ..models.account import Account, Role
from ..models.admin_details import AdminDetails, AdminRoleLevel
from ..models.organization_details import OrganizationDetails, VerificationStatus
from ..models.user_details import UserDetails, Gender, VerificationStatus as UserVerificationStatus
from ..extensions import db

# إعداد السجل للتصحيح
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()
fake = Faker('ar_PS') 

# إعدادات قاعدة البيانات
db_config = {
    'host': os.getenv('MYSQL_DATABASE_HOST', '127.0.0.1'),
    'user': os.getenv('MYSQL_DATABASE_USER', 'your_username'),
    'password': os.getenv('MYSQL_DATABASE_PASSWORD', 'your_password'),
    'database': os.getenv('MYSQL_DATABASE_DB', 'giveandgrow')
}



# قائمة المدن الفلسطينية
cities = [
    'Ramallah', 'Nablus', 'Hebron', 'Gaza', 'Jerusalem', 'Jenin',
    'Bethlehem', 'Tulkarm', 'Qalqilya', 'Salfit', 'Tubas', 'Rafah',
    'Khan Yunis', 'Deir al-Balah', 'Beit Lahia', 'Beit Hanoun',
    'Bani Suheila', 'Dura', 'Yatta', 'Halhul', 'Anabta', 'Azzun',
    'Balata', 'Al-Bireh', 'Abu Dis', 'Birzeit', 'Beit Jala',
    'Beit Sahour', 'Al-Eizariya', 'Al-Zahra', 'Al-Mughraqa',
    'Al-Nuseirat', 'Maghazi', 'Al-Burij', 'Jabalia', 'Zawata',
    'Askar', 'Tell', 'Qabatiya', 'Arraba', 'Sanur', 'Kafr Qaddum',
    'Jayyous', "Ni'lin", 'Beitunia', 'Idna', "Sa'ir", 'Tarqumiya',
    'Qatanna', 'Biddu', 'Hizma'
]

# أسماء ذكور وإناث
male_names_ar_en = [
    "Mohammed", "Ahmed", "Ali", "Hassan", "Omar", "Khaled", "Sami", "Youssef", "Tariq", "Zaid",
    "Nasser", "Faris", "Rami", "Basil", "Jamal", "Ayman", "Salah", "Ibrahim", "Walid", "Karim",
    "Majid", "Rashid", "Salim", "Fahad", "Adel", "Mahmoud", "Saif", "Anas", "Amir", "Hani",
    "Hussein", "Nabil", "Samir", "Bilal", "Ziyad", "Mustafa", "Abdel", "Bassam", "Kamal", "Mazen",
    "Nader", "Othman", "Qasim", "Riyad", "Saber", "Talal", "Yasin", "Zakaria", "Fawzi", "Jihad"
]

female_names_ar_en = [
    "Fatima", "Aisha", "Noor", "Layla", "Mariam", "Salma", "Rania", "Sara", "Huda", "Dina",
    "Nour", "Amal", "Lina", "Yasmin", "Jumana", "Reem", "Hanan", "Wafa", "Ruba", "Kholoud",
    "Sahar", "Mona", "Dana", "Laila", "Manal", "Nahla", "Rasha", "Hiba", "Shatha", "Nada",
    "Aya", "Nadeen", "Rima", "Sana", "Tahani", "Zainab", "Lubna", "Maha", "Samira", "Dalia",
    "Farah", "Amani", "Basima", "Eman", "Ghada", "Ibtisam", "Jana", "Kenza", "Lamis", "Marwa"
]

# أسماء المؤسسات
org_names = [
    'Hope Foundation', 'Tech for Good', 'Community Builders', 'Green Palestine',
    'Youth Empowerment Org', 'Health First', 'Education for All',
    'Future Innovators', 'Palestine Volunteers Network', 'Women Rise Initiative',
    'Code for Change', 'Medical Aid Group', 'EcoVision Palestine', 'Bright Minds',
    'Hands of Solidarity', 'Bridge the Gap', 'Green Roots', 'SkillUp Palestine',
    'Safe Steps', 'Youth Leaders United', 'Tomorrow’s Builders', 'Justice Now',
    'Care and Share', 'Rebuild Gaza', 'Voices of Hope', 'Inspire Youth',
    'Digital Uplift', 'Together Stronger', 'Tech Volunteers Org', 'Healthy Future',
    'Dream Makers', 'Peace in Action', 'Art for Impact', 'EduPal', 'Bright Horizons',
    'The Learning Hub', 'She Leads', 'NextGen Volunteers', 'Pal Relief Team',
    'Support & Serve', 'Innovation for All', 'United for Change', 'Heart & Hand Org',
    'Build Better Lives', 'Green Tomorrow', 'TalentGrow', 'Access for All',
    'Digital Palestine', 'Lead Forward', 'Together We Can'
]

# ✅ أدوات مساعدة
def random_gender():
    return random.choice([Gender.MALE, Gender.FEMALE])

def random_city():
    return random.choice(cities)

def get_arabic_first_name_en(gender):
    if gender == Gender.MALE:
        return random.choice(male_names_ar_en)
    else:
        return random.choice(female_names_ar_en)   

def generate_palestinian_phone():
    prefix = random.choice(["059", "056"])
    suffix = "".join([str(random.randint(0, 9)) for _ in range(7)])
    return prefix + suffix

# 🛠 Seeder Function
def seed_accounts():
    print("🔄 Seeding accounts...")

    # أدمنز
    for i in range(3):
        email = f"admin{i+1}@givandgrow.com"
        account = Account(email=email, role=Role.ADMIN, is_email_verified=True)
        account.set_password("Admin123!")

        gender = random_gender()
        name = get_arabic_first_name_en(gender)

        admin = AdminDetails(
            account=account,
            name=name,
            role_level=random.choice(list(AdminRoleLevel))
        )

        db.session.add(account)
        db.session.add(admin)

    # مؤسسات
    for i in range(20):
        name = random.choice(org_names)  
        email = f"org{i+1}@givandgrow.com"
        username = f"{name.split(' ')[0]}{i+1}"
        account = Account(email=email, role=Role.ORGANIZATION, username=username, is_email_verified=True)
        account.set_password("Orga123!")

        org = OrganizationDetails(
            account=account,
            name=name,
            description=fake.text(max_nb_chars=100),
            phone=generate_palestinian_phone(),
            address=random_city(),
            proof_verification_status=random.choice(list(VerificationStatus))
        )

        db.session.add(account)
        db.session.add(org)

    # مستخدمين
    for i in range(100):
        gender = random_gender()
        first_name = get_arabic_first_name_en(gender)
        last_name = get_arabic_first_name_en(Gender.MALE)
        email = f"{first_name.lower()}_{last_name.lower()}@gmail.com"
        
        
        username = f"{first_name}{i+1}"
        account = Account(email=email, role=Role.USER, username=username, is_email_verified=True)
        account.set_password("User123!")


        user = UserDetails(
            account=account,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=40),
            phone_number=generate_palestinian_phone(),
            city=random_city(),
            country="Palestine",
            bio=fake.sentence(nb_words=12),
            identity_verification_status=random.choice(list(UserVerificationStatus)),
            rank="First",
            total_points=0,
            current_points=0
        )

        db.session.add(account)
        db.session.add(user)

    db.session.commit()
    print("✅ Accounts seeding complete!")

# استدعاء دالة seeding
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    print("🔄 Seeding accounts...")
    seed_accounts()
    print("✅ Seeding completed.")