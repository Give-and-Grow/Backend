# Backend/app/config.py
import os
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials, firestore, messaging
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MYSQL_DATABASE_USER')}:"
        f"{os.getenv('MYSQL_DATABASE_PASSWORD')}@"
        f"{os.getenv('MYSQL_DATABASE_HOST')}:"
        f"{os.getenv('MYSQL_DATABASE_PORT')}/"
        f"{os.getenv('MYSQL_DATABASE_DB')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "123")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "baraa.shellbaya@gmail.com")
    APYHUB_API_KEY = os.getenv("APYHUB_API_KEY")


cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIAL_PATH"))
firebase_admin.initialize_app(cred)

db_firestore = firestore.client()
