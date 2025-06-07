# Backend/app/seeds/seed_admins_only.py

import random
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models.account import Account, Role
from app.models.admin_details import AdminDetails, AdminRoleLevel

# أسماء عربية إنجليزية
admin_names = [
    "Mohammed", "Ahmed", "Ali", "Hassan", "Omar", "Khaled", "Sami", "Youssef", "Tariq", "Zaid",
    "Fatima", "Aisha", "Noor", "Layla", "Mariam", "Salma", "Rania", "Sara", "Huda", "Dina"
]
new_fcm_token = 'fo_b6ICPfYytDj4WfGvi11:APA91bEcXiizkv7gH_SMIFaNlz0L3oqLxqq49mzO_k-OWI0ijvjPmyKuCO5-kINhFk7HTBhl5dmDBBLmnMd8hUITBYErRBWg6zESL6mLQY-FjLE8Sa2Wg8A'

def seed_admins(count=5):
    print("🔄 Seeding admin accounts only...")

    # جلب أعلى id من جدول account
    last_account = Account.query.order_by(Account.id.desc()).first()
    last_account_id = last_account.id if last_account else 0

    # جلب أعلى account_id من جدول admin_details (للتأكد أكثر)
    last_admin = AdminDetails.query.order_by(AdminDetails.account_id.desc()).first()
    last_admin_id = last_admin.account_id if last_admin else 0

    # نأخذ الأعلى بين الاثنين
    start_id = max(last_account_id, last_admin_id) + 1

    for i in range(count):
        current_index = start_id + i
        name = random.choice(admin_names)
        email = f"admin{current_index}@giveandgrow.com"
        username = f"admin{current_index}"

        account = Account(
            email=email,
            role=Role.ADMIN,
            username=username,
            is_email_verified=True,
            is_active=True,
            created_at=datetime.now(),
            fcm_token=new_fcm_token
        )
        account.set_password("Admin.123#")

        admin_details = AdminDetails(
            account=account,
            name=name,
            role_level=random.choice(list(AdminRoleLevel)),
            is_active=True
        )

        db.session.add(account)
        db.session.add(admin_details)

    db.session.commit()
    print(f"✅ Done! {count} admin accounts inserted starting from ID {start_id}.")

# تفعيل السكربت
app = create_app()

with app.app_context():
    seed_admins(count=5)  # غير الرقم إذا بدك أكثر أو أقل
