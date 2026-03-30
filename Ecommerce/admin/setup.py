from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from Ecommerce.apps import database as db
from Ecommerce.apps.models.inventory_models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
    SeasonEvent,
    User,
)

from .views import CategoryView, ProductView


def Create_admin(app: Flask):
    # Init admin without template_mode for compatibility
    admin = Admin(app, name="Inventory Management System Admin")

    # Register views
    admin.add_view(CategoryView(Category, db.session))
    admin.add_view(ProductView(Product, db.session))
    admin.add_view(ModelView(ProductLine, db.session))
    admin.add_view(ModelView(ProductImage, db.session))
    admin.add_view(ModelView(SeasonEvent, db.session))
    admin.add_view(ModelView(Attribute, db.session))
    admin.add_view(ModelView(AttributeValue, db.session))
    admin.add_view(ModelView(ProductType, db.session))
    admin.add_view(ModelView(User, db.session))
