import os

import sqlalchemy as DataBase
from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from Ecommerce.celery_worker import celery_init_app
from Ecommerce.utils.extensions import login_manager

load_dotenv()
database = SQLAlchemy()
database_migratins = Migrate()
print("Project Started  ")


from apifairy import APIFairy
from celery.schedules import crontab
from flask_marshmallow import Marshmallow

database = SQLAlchemy()
database_migrations = Migrate()
marshmallow = Marshmallow()
apifairyobj = APIFairy()

mail = Mail()
cache = Cache()


def create_app(config_type=os.getenv("Config_Type")):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    app.config.from_object(config_type)

    database.init_app(app)
    database_migrations.init_app(app, database)

    from Ecommerce.apps.models import inventory_models  # noqa: F401

    marshmallow.init_app(app)

    # INITIALIZE LOGIN MANAGER FIRST
    login_manager.login_view = "login"
    login_manager.login_message = "Please log in to access admin panel"
    login_manager.init_app(app)

    register_blueprint(app)
    apifairyobj.init_app(app)

    # THEN Initialize Admin AFTER login_manager
    from Ecommerce.admin.setup import Create_admin

    Create_admin(app)

    app.config["CELERY"] = {
        "broker_url": os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"),
        "backend_url": os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"),
        "beat_schedule": {
            "every_20_seconds": {
                "task": "Ecommerce.tasks.task.Schduled_task_celery_beat",
                "schedule": 20,
            },
            "every_day_2_of_week": {
                "task": "Ecommerce.tasks.task.Schduled_task_celery__tow_day",
                "schedule": crontab(hour=2, minute=30, day_of_week=2),
            },
        },
        "redbeat_redis_url": "redis://127.0.0.1:6379/0",
    }
    celery_init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    return app


def register_blueprint(app):
    from Ecommerce.apps.inventory import (
        inventory_auth_api_blueprint,
        inventory_category_api_blueprint,
        inventory_prodcut_api_blueprint,
        inventory_user_api_blueprint,
    )

    app.register_blueprint(inventory_user_api_blueprint, url_prefix="/api")
    app.register_blueprint(inventory_category_api_blueprint, url_prefix="/api")
    app.register_blueprint(inventory_prodcut_api_blueprint, url_prefix="/api")
    app.register_blueprint(inventory_auth_api_blueprint, url_prefix="/api")
