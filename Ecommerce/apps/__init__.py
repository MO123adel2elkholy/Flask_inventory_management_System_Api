import sqlalchemy as DataBase
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from Ecommerce.celery_worker import celery_init_app

load_dotenv()
database = SQLAlchemy()
database_migratins = Migrate()
print("Project Started  ")


# def create_app(config_type=os.getenv("Config_Type")):
#     app = Flask(__name__)
#     app.config.from_object(config_type)
#     initialize_extensions(app)
#     return app


#  this for creating Databse instace for flask app


# def initialize_extensions(app):
#     database.init_app(app=app)
#     database_migratins.init_app(app=app, database=database)
#     from Ecommerce.apps.models import inventory_models  # noqa: F401


import os

from apifairy import APIFairy
from celery.schedules import crontab
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
database_migrations = Migrate()
marshmallow = Marshmallow()
apifairyobj = APIFairy()

mail = Mail()


def create_app(config_type=os.getenv("Config_Type")):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    app.config.from_object(config_type)

    database.init_app(app)
    database_migrations.init_app(app, database)

    from Ecommerce.apps.models import inventory_models  # noqa: F401

    marshmallow.init_app(app)
    register_blueprint(app)
    apifairyobj.init_app(app)
    app.config["CELERY"] = {
        "broker_url": os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"),
        "backend_url": os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"),
        "beat_schedule": {
            "every_20_seconds": {
                "task": "Ecommerce.tasks.task.Schduled_task_celery_beat",
                "schedule": 20,
                # 'args':(1,2)  this only when needed
            },
            "every_day_2_of_week": {
                "task": "Ecommerce.tasks.task.Schduled_task_celery__tow_day",
                "schedule": crontab(hour=2, minute=30, day_of_week=2),
                # 'args':(1,2)  this only when needed
            },
        },
        "redbeat_redis_url": "redis://127.0.0.1:6379/0",
    }
    celery_init_app(app)
    mail.init_app(app)

    return app


# Schduled_task_celery__tow_day


def register_blueprint(app):

    from Ecommerce.apps.inventory import (
        inventory_auth_api_blueprint,
        inventory_category_api_blueprint,  # noqa: F401
        inventory_prodcut_api_blueprint,  # noqa: F401
        inventory_user_api_blueprint,  # noqa: F401                       # noqa: F401; noqa: F401; noqa: F401; noqa: F401
    )

    app.register_blueprint(inventory_user_api_blueprint, url_prefix="/api")
    app.register_blueprint(inventory_category_api_blueprint, url_prefix="/api")
    app.register_blueprint(inventory_prodcut_api_blueprint, url_prefix="/api")
    app.register_blueprint(inventory_auth_api_blueprint, url_prefix="/api")
