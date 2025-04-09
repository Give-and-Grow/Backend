# app/utils/username.py
import random
import string
from ..models.user import User, db  

def generate_username(name, max_attempts=10):
    base = name.lower().replace(" ", "")
    for _ in range(max_attempts):
        suffix = random.randint(100, 999)
        username = f"{base}{suffix}"
        if not User.query.filter_by(username=username).first():
            return username
    while True:
        suffix = ''.join(random.choices(string.digits, k=6))
        username = f"{base}{suffix}"
        if not User.query.filter_by(username=username).first():
            return username