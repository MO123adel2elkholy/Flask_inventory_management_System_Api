import os

BaseDir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV")
    # DEBUG = os.getenv("DEBUG")
    DEBUG = True
    # Flask-Mail settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # استخدم env var
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # استخدم env var
    MAIL_DEFAULT_SENDER = ("Inventory System", MAIL_USERNAME)


class DevelopmentConfig(Config):
    # valid SQLAlchemy URI string pointing to a file inside the project
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BaseDir, 'ecommerce.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APIFAIRY_TITLE = "Ecommerce Project "
    APIFAIRY_UI = "swagger_ui"
    APIFAIRY_VERSION = "0.0.1"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(
        ","
    )  # Split the comma-separated string into a list
    CHATT_ROOMS = [
        "general",
        "random",
        "tech",
        "sports",
    ]


class ProductionConfig(Config):
    SECRET_KEY = "Product Key "
    FLASK_ENV = "Production"
    DEBUG = False


# ...existing code...
