import os

from itsdangerous import URLSafeTimedSerializer

SECRET_KEY = os.getenv("SECRET_KEY")

print(f"Your secret Key from envirnment varaibles is => {SECRET_KEY}")

serializer = URLSafeTimedSerializer(SECRET_KEY)

print(f" User Serializer {serializer}")


def generate_token(email):
    return serializer.dumps(email, salt="email-confirm")


def verify_token(token, max_age=3600):
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=max_age)
        return email
    except:
        return None
