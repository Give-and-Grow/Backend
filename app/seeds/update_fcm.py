import mysql.connector
from dotenv import load_dotenv
import os

def main():
    # تحميل متغيرات البيئة من ملف .env (استخدم raw string لتجنب مشاكل المسارات)
    load_dotenv(r"C:\Users\Bara'a\Desktop\GivandGrow\Backend\.env")

    # طباعة المتغيرات للتأكد من تحميلها (يمكن حذف هذه الطباعة لاحقًا)
    print("MYSQL_DATABASE_HOST:", os.getenv('MYSQL_DATABASE_HOST'))
    print("MYSQL_DATABASE_PORT:", os.getenv('MYSQL_DATABASE_PORT'))
    print("MYSQL_DATABASE_USER:", os.getenv('MYSQL_DATABASE_USER'))
    print("MYSQL_DATABASE_PASSWORD:", os.getenv('MYSQL_DATABASE_PASSWORD'))
    print("MYSQL_DATABASE_DB:", os.getenv('MYSQL_DATABASE_DB'))

    try:
        # إنشاء الاتصال بقاعدة البيانات
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_DATABASE_HOST'),
            port=int(os.getenv('MYSQL_DATABASE_PORT')),
            user=os.getenv('MYSQL_DATABASE_USER'),
            password=os.getenv('MYSQL_DATABASE_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE_DB')
        )

        cursor = conn.cursor()

        # القيمة الجديدة لـ fcm_token
        new_fcm_token = 'fo_b6ICPfYytDj4WfGvi11:APA91bEcXiizkv7gH_SMIFaNlz0L3oqLxqq49mzO_k-OWI0ijvjPmyKuCO5-kINhFk7HTBhl5dmDBBLmnMd8hUITBYErRBWg6zESL6mLQY-FjLE8Sa2Wg8A'

        # استعلام التحديث
        update_query = "UPDATE account SET fcm_token = %s"

        cursor.execute(update_query, (new_fcm_token,))
        conn.commit()
        print("✅ fcm_token updated for all accounts.")

    except Exception as e:
        print(f"❌ Error updating fcm_token: {e}")

    finally:
        # تأكد من إغلاق الاتصال حتى لو حدث خطأ
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
