import os
from dotenv import load_dotenv
import random
from faker import Faker
import bcrypt
import mysql.connector
from datetime import datetime, timedelta
import logging
import uuid

# إعداد logging لتتبع التقدم
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# تحميل متغيرات البيئة من .env
load_dotenv()

# تهيئة Faker لتوليد بيانات واقعية
fake = Faker()

# إعدادات الاتصال بقاعدة البيانات
db_config = {
    'host': os.getenv('MYSQL_DATABASE_HOST', '127.0.0.1'),
    'user': os.getenv('MYSQL_DATABASE_USER', 'your_username'),
    'password': os.getenv('MYSQL_DATABASE_PASSWORD', 'your_password'),
    'database': os.getenv('MYSQL_DATABASE_DB', 'giveandgrow')
}

# الاتصال بقاعدة البيانات
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    logger.info("Connected to database successfully!")
except mysql.connector.Error as err:
    logger.error(f"Failed to connect to database: {err}")
    exit(1)

# دالة لتشفير كلمات المرور
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# قوائم لتوليد البيانات
cities = ['Ramallah', 'Nablus', 'Hebron', 'Gaza', 'Jerusalem', 'Jenin', 'Bethlehem', 'Tulkarm']
skills_list = ['Python', 'JavaScript', 'Project Management', 'Event Planning', 'Web Development', 
               'Data Analysis', 'Graphic Design', 'Teaching', 'Fundraising', 'Marketing']
tags_list = ['education', 'remote', 'healthcare', 'technology', 'community', 'environment', 'youth']
roles = ['USER', 'ORGANIZATION', 'ADMIN']
org_names = ['Hope Foundation', 'Tech for Good', 'Community Builders', 'Green Palestine', 
             'Youth Empowerment Org', 'Health First', 'Education for All']
statuses = ['OPEN', 'CLOSED', 'FILLED']
genders = ['MALE', 'FEMALE']
period_types = ['MONTH', 'SMONTH', 'YEAR']
attendance_statuses = ['attended', 'absent', 'late', 'excused']
industries = ['Education', 'Healthcare', 'Technology', 'Environment', 'Community Development']

# 1. تعبئة جدول skill
logger.info("Inserting skills...")
for skill in skills_list:
    try:
        cursor.execute("INSERT IGNORE INTO skill (name) VALUES (%s)", (skill,))
        logger.info(f"Inserted skill: {skill}")
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting skill {skill}: {err}")
conn.commit()

# 2. تعبئة جدول tag
logger.info("Inserting tags...")
for tag in tags_list:
    try:
        cursor.execute("INSERT IGNORE INTO tag (name) VALUES (%s)", (tag,))
        logger.info(f"Inserted tag: {tag}")
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting tag {tag}: {err}")
conn.commit()

# 3. تعبئة جدول account
num_users = 200
num_orgs = 10
num_admins = 5
logger.info(f"Inserting {num_users} users, {num_orgs} organizations, {num_admins} admins...")
for i in range(num_users + num_orgs + num_admins):
    email = fake.email()
    username = fake.user_name() + str(random.randint(100, 999))
    password = hash_password('password123')
    role = 'USER' if i < num_users else 'ORGANIZATION' if i < num_users + num_orgs else 'ADMIN'
    is_email_verified = random.choice([0, 1])
    verification_code = str(random.randint(100000, 999999)) if not is_email_verified else None
    verification_code_expiry = (datetime.now() + timedelta(days=1)) if verification_code else None
    created_at = fake.date_time_this_year()
    updated_at = fake.date_time_this_year() if random.choice([True, False]) else None
    last_login = fake.date_time_this_year() if random.choice([True, False]) else None

    try:
        cursor.execute("""
            INSERT IGNORE INTO account (email, password, username, role, is_email_verified, verification_code, 
                                       verification_code_expiry, created_at, updated_at, last_login)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (email, password, username, role, is_email_verified, verification_code, 
              verification_code_expiry, created_at, updated_at, last_login))
        if (i + 1) % 100 == 0:
            logger.info(f"Inserted {i + 1} accounts")
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting account {email}: {err}")
conn.commit()
logger.info("Finished inserting accounts")

# جلب معرفات الحسابات
cursor.execute("SELECT id, role FROM account")
accounts = cursor.fetchall()
user_accounts = [acc[0] for acc in accounts if acc[1] == 'USER']
org_accounts = [acc[0] for acc in accounts if acc[1] == 'ORGANIZATION']
admin_accounts = [acc[0] for acc in accounts if acc[1] == 'ADMIN']
logger.info(f"Fetched {len(user_accounts)} user accounts, {len(org_accounts)} org accounts, {len(admin_accounts)} admin accounts")

# 4. تعبئة جدول admin_details
logger.info("Inserting admin_details...")
cursor.execute("SELECT id FROM account WHERE role = 'ADMIN'")
admin_accounts = cursor.fetchall()
for acc in admin_accounts:
    account_id = acc[0]  # acc هو tuple يحتوي على id فقط
    name = "Admin"
    role_level = "SUPERADMIN"
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute("""
            INSERT INTO admin_details (account_id, name, role_level, updated_at)
            VALUES (%s, %s, %s, %s)
        """, (account_id, name, role_level, updated_at))
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting admin_details for account_id {account_id}: {err}")
conn.commit()
logger.info("Finished inserting admin_details")

# 5. تعبئة جدول user_details
logger.info("Inserting user_details...")
for user_id in user_accounts:
    name = fake.first_name()
    last_name = fake.last_name()
    phone_number = fake.phone_number()[:15]
    gender = random.choice(genders)
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=60)
    city = random.choice(cities)
    village = fake.city() if random.choice([True, False]) else ''
    bio = fake.text(max_nb_chars=200) if random.choice([True, False]) else None
    profile_picture = fake.image_url() if random.choice([True, False]) else None
    experience = fake.text(max_nb_chars=200) if random.choice([True, False]) else None
    identity_picture = fake.image_url() if random.choice([True, False]) else None
    identity_verification_status = random.choice(['PENDING', 'APPROVED', 'REJECTED'])
    total_points = random.randint(0, 1000)
    current_points = random.randint(0, total_points)
    latitude = random.uniform(31.0, 32.5)
    longitude = random.uniform(34.0, 35.5)
    country = 'Palestinian Territory'

    try:
        cursor.execute("""
            INSERT IGNORE INTO user_details (account_id, name, last_name, phone_number, gender, date_of_birth, 
                                            city, village, bio, profile_picture, experience, identity_picture, 
                                            identity_verification_status, total_points, current_points, country, 
                                            latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, name, last_name, phone_number, gender, date_of_birth, city, village, bio, 
              profile_picture, experience, identity_picture, identity_verification_status, 
              total_points, current_points, country, latitude, longitude))
        logger.info(f"Inserted user_details for account_id {user_id}")
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting user_details for account_id {user_id}: {err}")
conn.commit()
logger.info("Finished inserting user_details")

# 6. تعبئة جدول organization_details
logger.info("Inserting organization_details...")
for org_id in org_accounts:
    name = random.choice(org_names) + str(random.randint(100, 999))
    description = fake.text(max_nb_chars=500)
    phone = fake.phone_number()[:15]
    proof_verification_status = random.choice(['PENDING', 'APPROVED', 'REJECTED'])
    logo = fake.image_url() if random.choice([True, False]) else None
    proof_image = fake.image_url() if random.choice([True, False]) else None

    try:
        cursor.execute("""
            INSERT IGNORE INTO organization_details (account_id, name, description, logo, phone, 
                                                   proof_image, proof_verification_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (org_id, name, description, logo, phone, proof_image, proof_verification_status))
        logger.info(f"Inserted organization_details for account_id {org_id}")
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting organization_details for account_id {org_id}: {err}")
conn.commit()
logger.info("Finished inserting organization_details")

# جلب معرفات user_details و organization_details
cursor.execute("SELECT id, account_id FROM user_details")
user_details = cursor.fetchall()
user_details_ids = [ud[0] for ud in user_details]
cursor.execute("SELECT id, account_id FROM organization_details")
org_details = cursor.fetchall()
org_details_ids = [od[0] for od in org_details]
logger.info(f"Fetched {len(user_details_ids)} user_details, {len(org_details_ids)} organization_details")

# 7. تعبئة جدول user_skills
cursor.execute("SELECT id FROM skill")
skill_ids = [row[0] for row in cursor.fetchall()]
logger.info("Inserting user_skills...")
for user_id in user_details_ids:
    num_skills = random.randint(1, 5)
    user_skills = random.sample(skill_ids, num_skills)
    for skill_id in user_skills:
        try:
            cursor.execute("INSERT IGNORE INTO user_skills (user_id, skill_id) VALUES (%s, %s)", 
                          (user_id, skill_id))
        except mysql.connector.Error as err:
            logger.warning(f"Error inserting user_skill for user_id {user_id}, skill_id {skill_id}: {err}")
conn.commit()
logger.info("Finished inserting user_skills")

# 8. تعبئة جدول opportunity
num_opportunities = 1000
logger.info(f"Inserting {num_opportunities} opportunities...")
for i in range(num_opportunities):
    org_id = random.choice(org_details_ids)
    opportunity_type = 'VOLUNTEER' if random.random() < 0.7 else 'JOB'
    title = f"{opportunity_type.title()} Opportunity {i+1}"
    description = fake.text(max_nb_chars=500)
    location = random.choice(cities)
    start_date = fake.date_between(start_date='today', end_date='+1y')
    end_date = start_date + timedelta(days=random.randint(1, 90))
    status = random.choice(statuses)
    image_url = fake.image_url() if opportunity_type == 'VOLUNTEER' else None
    application_link = fake.url() if opportunity_type == 'VOLUNTEER' else None
    contact_email = fake.email()
    latitude = random.uniform(31.0, 32.5)
    longitude = random.uniform(34.0, 35.5)
    is_deleted = random.choice([0, 1]) if random.random() < 0.1 else 0

    try:
        cursor.execute("""
            INSERT IGNORE INTO opportunity (organization_id, title, description, location, start_date, end_date, 
                                           status, image_url, application_link, contact_email, opportunity_type, 
                                           latitude, longitude, is_deleted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (org_id, title, description, location, start_date, end_date, status, image_url, 
              application_link, contact_email, opportunity_type, latitude, longitude, is_deleted))
        if (i + 1) % 100 == 0:
            logger.info(f"Inserted {i + 1} opportunities")
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting opportunity {title}: {err}")
conn.commit()
logger.info("Finished inserting opportunities")

# جلب معرفات الفرص
cursor.execute("SELECT id, opportunity_type FROM opportunity")
opportunities = cursor.fetchall()
volunteer_opp_ids = [opp[0] for opp in opportunities if opp[1] == 'VOLUNTEER']
job_opp_ids = [opp[0] for opp in opportunities if opp[1] == 'JOB']
logger.info(f"Fetched {len(volunteer_opp_ids)} volunteer opportunities, {len(job_opp_ids)} job opportunities")

# 9. تعبئة جدول volunteer_opportunity
logger.info("Inserting volunteer_opportunities...")
for opp_id in volunteer_opp_ids:
    max_participants = random.randint(10, 100)
    base_points = random.randint(50, 200)
    current_participants = random.randint(0, max_participants)

    try:
        cursor.execute("""
            INSERT IGNORE INTO volunteer_opportunity (opportunity_id, max_participants, base_points, current_participants)
            VALUES (%s, %s, %s, %s)
        """, (opp_id, max_participants, base_points, current_participants))
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting volunteer_opportunity for opportunity_id {opp_id}: {err}")
conn.commit()
logger.info("Finished inserting volunteer_opportunities")

# 10. تعبئة جدول job_opportunity
logger.info("Inserting job_opportunities...")
for opp_id in job_opp_ids:
    required_points = random.randint(100, 1000)

    try:
        cursor.execute("""
            INSERT IGNORE INTO job_opportunity (opportunity_id, required_points)
            VALUES (%s, %s)
        """, (opp_id, required_points))
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting job_opportunity for opportunity_id {opp_id}: {err}")
conn.commit()
logger.info("Finished inserting job_opportunities")

# 11. تعبئة جدول opportunity_skills
logger.info("Inserting opportunity_skills...")
for opp_id in [opp[0] for opp in opportunities]:
    num_skills = random.randint(1, 4)
    opp_skills = random.sample(skill_ids, num_skills)
    for skill_id in opp_skills:
        try:
            cursor.execute("INSERT IGNORE INTO opportunity_skills (opportunity_id, skill_id) VALUES (%s, %s)", 
                          (opp_id, skill_id))
        except mysql.connector.Error as err:
            logger.warning(f"Error inserting opportunity_skill for opportunity_id {opp_id}, skill_id {skill_id}: {err}")
conn.commit()
logger.info("Finished inserting opportunity_skills")

# 12. تعبئة جدول opportunity_tags
cursor.execute("SELECT id FROM tag")
tag_ids = [row[0] for row in cursor.fetchall()]
logger.info("Inserting opportunity_tags...")
for opp_id in [opp[0] for opp in opportunities]:
    num_tags = random.randint(1, 3)
    opp_tags = random.sample(tag_ids, num_tags)
    for tag_id in opp_tags:
        try:
            cursor.execute("INSERT IGNORE INTO opportunity_tags (opportunity_id, tag_id) VALUES (%s, %s)", 
                          (opp_id, tag_id))
        except mysql.connector.Error as err:
            logger.warning(f"Error inserting opportunity_tag for opportunity_id {opp_id}, tag_id {tag_id}: {err}")
conn.commit()
logger.info("Finished inserting opportunity_tags")

# 13. تعبئة جدول user_achievement
logger.info("Inserting user_achievements...")
for user_id in user_details_ids:
    num_achievements = random.randint(0, 5)
    for _ in range(num_achievements):
        title = f"Achievement {fake.word().capitalize()}"
        description = fake.text(max_nb_chars=200)
        badge_icon = fake.image_url()
        period_type = random.choice(period_types)
        period_date = fake.date_this_year()

        try:
            cursor.execute("""
                INSERT IGNORE INTO user_achievement (user_id, title, description, badge_icon, period_type, period_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, title, description, badge_icon, period_type, period_date))
        except mysql.connector.Error as err:
            logger.warning(f"Error inserting user_achievement for user_id {user_id}: {err}")
conn.commit()
logger.info("Finished inserting user_achievements")

# 14. تعبئة جدول user_points
logger.info("Inserting user_points...")
for user_id in user_details_ids:
    num_entries = random.randint(1, 12)
    for _ in range(num_entries):
        total_points = random.randint(50, 500)
        month = fake.month()
        year = random.randint(2023, 2025)

        try:
            cursor.execute("""
                INSERT IGNORE INTO user_points (user_id, total_points, month, year)
                VALUES (%s, %s, %s, %s)
            """, (user_id, total_points, month, year))
        except mysql.connector.Error as err:
            logger.warning(f"Error inserting user_points for user_id {user_id}: {err}")
conn.commit()
logger.info("Finished inserting user_points")

# 15. تعبئة جدول industry
logger.info("Inserting industries...")
for industry in industries:
    try:
        cursor.execute("INSERT IGNORE INTO industry (name) VALUES (%s)", (industry,))
        logger.info(f"Inserted industry: {industry}")
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting industry {industry}: {err}")
conn.commit()

# جلب معرفات الصناعات
cursor.execute("SELECT id FROM industry")
industry_ids = [row[0] for row in cursor.fetchall()]

# 16. تعبئة جدول organization_industry
logger.info("Inserting organization_industry relations...")
for org_id in org_details_ids:
    num_industries = random.randint(1, 3)
    selected_industries = random.sample(industry_ids, num_industries)
    for industry_id in selected_industries:
        try:
            cursor.execute("""
                INSERT IGNORE INTO organization_industry (organization_id, industry_id)
                VALUES (%s, %s)
            """, (org_id, industry_id))
        except mysql.connector.Error as err:
            logger.warning(f"Error linking organization {org_id} to industry {industry_id}: {err}")
conn.commit()
logger.info("Finished inserting organization_industry relations")

# 17. تعبئة جدول opportunity_participant
logger.info("Inserting opportunity_participant...")
attendance_points_map = {
    "attended": 100,
    "late": 70,
    "excused": 50,
    "absent": 0
}
num_participants = 2000
for _ in range(num_participants):
    opportunity_id = random.choice(volunteer_opp_ids)
    user_id = random.choice(user_details_ids)
    joined_at = fake.date_time_this_year()
    rating = random.randint(1, 5) if random.random() < 0.8 else None
    completed = random.choice([0, 1])
    feedback = fake.text(max_nb_chars=200) if random.random() < 0.5 else None
    attendance_status = random.choice(attendance_statuses)
    rated_at = fake.date_time_this_year() if rating else None

    # جلب النقاط الأساسية من volunteer_opportunity
    cursor.execute("SELECT base_points FROM volunteer_opportunity WHERE opportunity_id = %s", (opportunity_id,))
    result = cursor.fetchone()
    base_points = result[0] if result else 100

    # حساب النقاط بناءً على الحضور والتقييم
    attendance_percentage = attendance_points_map.get(attendance_status, 0)
    attendance_score = (attendance_percentage / 100) * (0.4 * base_points)
    rating_score = (rating / 5) * (0.6 * base_points) if rating else 0
    points_earned = int(attendance_score + rating_score)

    try:
        cursor.execute("""
            INSERT IGNORE INTO opportunity_participant (opportunity_id, user_id, joined_at, rating, completed, 
                                                      points_earned, feedback, attendance_status, rated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (opportunity_id, user_id, joined_at, rating, completed, points_earned, feedback, attendance_status, rated_at))
    except mysql.connector.Error as err:
        logger.warning(f"Error inserting opportunity_participant for opportunity_id {opportunity_id}, user_id {user_id}: {err}")
conn.commit()
logger.info("Finished inserting opportunity_participant")

# إغلاق الاتصال
cursor.close()
conn.close()
logger.info("Database populated successfully!")