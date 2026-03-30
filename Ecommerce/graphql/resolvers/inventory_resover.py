from ariadne import MutationType, ObjectType, QueryType

from Ecommerce.apps import database as db
from Ecommerce.apps.models.inventory_models import Category, Product, User
from Ecommerce.Limiter.decorators.graphql_rate_limit_decorator import graphql_rate_limit

query = QueryType()
mutation = MutationType()
product_obj = ObjectType("Product")

# -------- Queries --------


@query.field("users")
def get_users(*_):
    return User.query.all()


@query.field("categories")
@graphql_rate_limit(limit=6, window=60 * 3)
def get_categories(*_):
    return Category.query.all()


@query.field("products")
@graphql_rate_limit(limit=2, window=60)
def get_products(*_):
    return Product.query.all()


@query.field("product")
@graphql_rate_limit(limit=5, window=120)
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
    return product
