from Ecommerce.apps.models.inventory_models import User
from Ecommerce.utils.extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
