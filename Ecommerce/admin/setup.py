# from flask import Flask
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

# from Ecommerce.admin.views import SecureModelView
# from Ecommerce.apps import database as db
# from Ecommerce.apps.models.inventory_models import (
#     Attribute,
#     AttributeValue,
#     Category,
#     Product,
#     ProductImage,
#     ProductLine,
#     ProductType,
#     SeasonEvent,
#     User,
# )

# from .views import CategoryView, ProductView


# def Create_admin(app: Flask):
#     # Init admin without template_mode for compatibility
#     admin = Admin(app, name="Inventory Management System Admin")

#     # Register views
#     admin.add_view(CategoryView(Category, db.session))
#     admin.add_view(ProductView(Product, db.session))
#     admin.add_view(ModelView(ProductLine, db.session))
#     admin.add_view(ModelView(ProductImage, db.session))
#     admin.add_view(ModelView(SeasonEvent, db.session))
#     admin.add_view(ModelView(Attribute, db.session))
#     admin.add_view(ModelView(AttributeValue, db.session))
#     admin.add_view(ModelView(ProductType, db.session))
#     admin.add_view(SecureModelView(User, db.session))


from flask import Flask
from flask_admin import Admin

from Ecommerce.admin.views import (
    AdminHomePageView,
    CategoryView,
    ProductView,
    SecureModelView,
)
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


def Create_admin(app: Flask):
    # Init admin without template_mode for compatibility
    admin = Admin(
        app, name="Inventory Management System Admin", index_view=AdminHomePageView()
    )

    # Register views - ALL using SecureModelView for security
    admin.add_view(CategoryView(Category, db.session))
    admin.add_view(ProductView(Product, db.session))
    admin.add_view(SecureModelView(ProductLine, db.session))
    admin.add_view(SecureModelView(ProductImage, db.session))
    admin.add_view(SecureModelView(SeasonEvent, db.session))
    admin.add_view(SecureModelView(Attribute, db.session))
    admin.add_view(SecureModelView(AttributeValue, db.session))
    admin.add_view(SecureModelView(ProductType, db.session))
    admin.add_view(SecureModelView(User, db.session))
