# from flask_admin.contrib.sqla import ModelView

# from Ecommerce.app import admin
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

# # Bootstrap for nice UI


# class CategoryView(ModelView):
#     column_list = ["id", "name", "slug", "parent_id"]  # Columns to display
#     column_searchable_list = ["name", "slug"]  # Searchable fields
#     column_filters = ["parent_id"]  # Filters
#     form_excluded_columns = ["children", "products"]  # Hide complex fields in forms


# class ProductView(ModelView):
#     column_list = ["id", "name", "price", "category"]
#     column_searchable_list = ["name"]
#     column_filters = ["category.name", "price"]
#     form_excluded_columns = ["productlines"]


# admin.add_view(CategoryView(Category, db.session))
# admin.add_view(ProductView(Product, db.session))
# admin.add_view(ModelView(ProductLine, db.session))
# admin.add_view(ModelView(ProductImage, db.session))
# admin.add_view(ModelView(SeasonEvent, db.session))
# admin.add_view(ModelView(Attribute, db.session))
# admin.add_view(ModelView(AttributeValue, db.session))
# admin.add_view(ModelView(ProductType, db.session))
# admin.add_view(ModelView(User, db.session))
