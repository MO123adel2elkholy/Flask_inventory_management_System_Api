from ariadne import MutationType, ObjectType, QueryType

from Ecommerce.apps import database as db
from Ecommerce.apps.models.inventory_models import Category, Product, User

query = QueryType()
mutation = MutationType()
product_obj = ObjectType("Product")

# -------- Queries --------


@query.field("users")
def get_users(*_):
    return User.query.all()


@query.field("categories")
def get_categories(*_):
    return Category.query.all()


@query.field("products")
def get_products(*_):
    return Product.query.all()


@query.field("product")
def get_product(_, info, id):
    return Product.query.get(id)


# -------- Relationship --------


@product_obj.field("category")
def resolve_product_category(obj, *_):
    return Category.query.get(obj.category)


# -------- Mutations --------


@mutation.field("createUser")
def create_user(_, info, username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


@mutation.field("createCategory")
def create_category(_, info, name, slug):
    cat = Category(name=name, slug=slug)
    db.session.add(cat)
    db.session.commit()
    return cat


@mutation.field("createProduct")
def create_product(_, info, name, slug, category_id):
    product = Product(name=name, slug=slug, category=category_id)
    db.session.add(product)
    db.session.commit()
    return product
