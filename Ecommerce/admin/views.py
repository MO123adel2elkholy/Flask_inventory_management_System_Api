from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AdminHomePageView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("inventory_auth_api_blueprint.login"))
        return "Unauthorized - Admin access required", 403


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("inventory_auth_api_blueprint.login"))
        return "Unauthorized - Admin access required", 403

    # ADD THESE - Enable pagination and data display
    page_size = 50
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class CategoryView(SecureModelView):
    column_list = ["id", "name", "slug", "parent_id"]
    column_searchable_list = ["name", "slug"]
    column_sortable_list = ["id", "name", "slug"]
    form_excluded_columns = ["children", "products"]

    # Display settings
    column_default_sort = ("id", False)
    page_size = 20


class ProductView(SecureModelView):
    column_list = ["id", "name", "price", "category"]
    column_searchable_list = ["name"]
    column_sortable_list = ["id", "name"]
    form_excluded_columns = ["productlines"]

    # Display settings
    column_default_sort = ("id", False)
    page_size = 20
