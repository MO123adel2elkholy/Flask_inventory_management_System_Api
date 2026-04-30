class APIException(Exception):
    def init(self, message, status_code):
        self.message = message
        self.status_code = status_code


# from Ecommerce.apps.models.inventory_models import User
# from Ecommerce.apps import database as db

# user = User.query.get(1)

# user.is_admin=True

# db.session.commit()
