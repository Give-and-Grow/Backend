import random

def generate_username(name):
    base = name.lower().replace(" ", "")
    suffix = random.randint(100, 999)
    return f"{base}{suffix}"