from flask_login import LoginManager

login_manager = LoginManager()


# ADD THIS - This is mandatory for Flask-Login to work
@login_manager.user_loader
def load_user(user_id):
    from Ecommerce.apps.models.inventory_models import User

    return User.query.get(int(user_id))
