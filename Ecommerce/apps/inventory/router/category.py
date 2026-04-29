from datetime import datetime, timedelta
from uuid import uuid4

from apifairy import body, response
from celery import current_app
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from redbeat import RedBeatSchedulerEntry

from Ecommerce.apps import cache
from Ecommerce.apps import database as db
from Ecommerce.apps.models.inventory_models import Category, Product, ProductImage
from Ecommerce.apps.schema.new_schema import (
    CategorySchema,
    CategorySchemaAuto,
    CategorySchemaAutoCrete,
    ProductSchema,
    productimage_schema,
)
from Ecommerce.tasks.task import Sleeping, make_image  # noqa: F401
from Ecommerce.utils.cash_key import categories_cache_keies, invalidate_categories_cache

# from Ecommerce.Exceptions import APIException
from .. import inventory_category_api_blueprint, inventory_prodcut_api_blueprint

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

categoryies_schema = CategorySchema(many=True)


def apply_query(query, args, model):

    page = args.get("page", 1, type=int)
    per_page = min(args.get("per_page", 10, type=int), 50)

    search = args.get("search")

    if search and hasattr(model, "name"):
        query = query.filter(model.name.ilike(f"%{search.strip()}%"))

    sort_by = args.get("sort_by", "id")
    order = args.get("order", "asc")

    if hasattr(model, sort_by):
        column = getattr(model, sort_by)
        query = query.order_by(column.desc() if order == "desc" else column.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return pagination  #


@inventory_category_api_blueprint.route("/category", methods=["GET"])
@jwt_required()
@cache.cached(timeout=50, key_prefix=categories_cache_keies)
def category():
    pagination = apply_query(Category.query, request.args, Category)
    return {
        "data": CategorySchemaAutoCrete(many=True).dump(pagination.items),
        "meta": {
            "page": pagination.page,
            "pages": pagination.pages,
            "total": pagination.total,
        },
    }


@inventory_prodcut_api_blueprint.route("/product", methods=["GET"])
@jwt_required()
@response(ProductSchema)
def product():
    return Product.query.all()


# create category
@inventory_category_api_blueprint.route("/category", methods=["POST"])
@body(CategorySchemaAuto(many=False))
@jwt_required()
@response(category_schema)
def create_category(data):
    data = request.get_json()
    print(f"data=> {data['name']} ")
    # Sleeping.apply_async(
    #     args=(data["name"],), countdown=10
    # )  # Schedule the task to run after 10 seconds
    Sleeping.apply_async(
        args=(data["name"],), eta=datetime.utcnow() + timedelta(minutes=1)
    )  # Schedule the task to run after 10 seconds
    category = Category(**data)
    db.session.add(category)
    db.session.commit()
    invalidate_categories_cache()
    return category


# get category by id


@inventory_category_api_blueprint.route("/category/<int:id>", methods=["GET"])
@jwt_required()
@response(category_schema)
def get_category(id):
    try:
        category = Category.query.get(id)
        print(f"category {category}")
        return category
    except:
        return {"message": "not found ", "status_Code": 404}


# delete category
@inventory_category_api_blueprint.route("/category/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_category(id):
    category = Category.query.get(id)
    print(f"category {category}")
    if category:
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted", "status_Code": 204}
    else:
        return {"message": "not found ", "status_Code": 404}


@inventory_category_api_blueprint.route("/category/<int:category_id>", methods=["PUT"])
@body(CategorySchemaAuto(many=False))  # body من العميل
@jwt_required()
@response(category_schema)  # Changed to category_schema for output
def update_category_full(body, category_id):
    """
    تحديث كامل للـ category.
    """
    category = Category.query.get_or_404(category_id)

    # مسح كل الحقول القديمة واستبدالها بالجديدة
    for key, value in vars(body).items():
        if not key.startswith("_"):
            setattr(category, key, value)

    db.session.commit()
    return category


# تحديث جزئي - PATCH
@inventory_category_api_blueprint.route(
    "/category/<int:category_id>", methods=["PATCH"]
)
@body(CategorySchemaAuto(many=False, partial=True))  # partial=True يسمح بتحديث جزئي
@jwt_required()
@response(category_schema)  # Changed to category_schema for output
def update_category_partial(body, category_id):
    """
    تحديث جزئي للـ category.
    """
    category = Category.query.get_or_404(category_id)

    # تحديث الحقول الموجودة فقط
    for key, value in vars(body).items():
        if not key.startswith("_"):
            setattr(category, key, value)

    db.session.commit()
    return category


# ...existing code...

# ...existing code...

from celery.schedules import crontab
from flask.json import jsonify

from Ecommerce.apps.schema.new_schema import CategorySchemaAuto


# Add this route inside your app definition (e.g., after app = Flask(__name__))
@inventory_category_api_blueprint.route(
    "/test-category/<int:category_id>", methods=["GET"]
)
@jwt_required()
def test_Celery_red_beat_Dynamic_schedule(
    category_id,
):
    category = Category.query.get_or_404(category_id)  # Fetch category by ID
    schema = CategorySchemaAutoCrete(many=False)
    result = schema.dump(category)
    dt = datetime.utcnow()
    # interval = rrule(freq="MNIUTELY", dtstart=dt)   custome Scheduling
    interval = crontab(minute="*")

    schedule_name = str(uuid4())
    task = "Ecommerce.tasks.task.Red_beat_Schedule_task"
    entry = RedBeatSchedulerEntry(
        schedule_name,
        task,
        interval,
        args=["from Schedule printed "],
        kwargs={"schedule_name": schedule_name},
        app=current_app,
    )
    entry.save()
    return jsonify(result)  # Returns JSON with subcategories and products


# create Product Image


@inventory_prodcut_api_blueprint.route("/productimage", methods=["POST"])
@body(productimage_schema)
@jwt_required()
@response(productimage_schema)
def product_image(data):
    data = request.get_json()
    print(f"data =>{data}")
    # make_image.delay(data['alt_txt'])
    productline_image = ProductImage(**data)
    db.session.add(productline_image)
    db.session.commit()
    return productline_image
