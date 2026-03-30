from flask_admin.contrib.sqla import ModelView


# Category Admin View
class CategoryView(ModelView):
    column_list = ["id", "name", "slug", "parent_id"]
    column_searchable_list = ["name", "slug"]
    # column_filters = ["parent_id"]
    form_excluded_columns = ["children", "products"]


# Product Admin View
class ProductView(ModelView):
    column_list = ["id", "name", "price", "category"]
    column_searchable_list = ["name"]
    # column_filters = ["category.name", "price"]
    form_excluded_columns = ["productlines"]
