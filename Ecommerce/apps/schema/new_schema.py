# Ecommerce.apps import marshmallow
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

from Ecommerce.apps.models.inventory_models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    Product_ProductType,
    ProductImage,
    ProductLine,
    ProductLine_Attribute,
    ProductType,
    SeasonEvent,
    User,
)

ma = Marshmallow()


class CategorySchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    slug = ma.String(required=True)


# Ecommerce.apps import marshmallow


class CategorySchemaAutoCrete(ma.SQLAlchemyAutoSchema):
    parent_id = fields.Int(allow_none=True)

    children = fields.Nested(lambda: CategorySchema, many=True)

    products = fields.Nested(
        "ProductSchema",
        many=True,
    )
    parent = fields.Nested(lambda: CategorySchema())

    class Meta:
        model = Category
        load_instance = True
        include_fk = True


class CategoryPaginationSchema(Schema):
    data = fields.List(fields.Nested(CategorySchemaAutoCrete))
    meta = fields.Dict()


# Base schemas using ma.SQLAlchemyAutoSchema for automatic field generation
# for update (partial and full )and creaete ()
class CategorySchemaAuto(ma.SQLAlchemyAutoSchema):
    parent_id = fields.Int(allow_none=True)

    children = fields.Nested("self", many=True, dump_only=True)

    products = fields.Nested("ProductSchema", many=True, dump_only=True)
    parent = fields.Nested(lambda: CategorySchema(), allow_none=True)

    class Meta:
        model = Category
        load_instance = True
        include_fk = True

    # Handle self-referential parent


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True

    # Nested relationships
    category = fields.Nested(CategorySchema, exclude=("products",))
    seasonevent = fields.Nested("SeasonEventSchema", allow_none=True)


class ProductLineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductLine
        load_instance = True
        include_fk = True

    # Nested product
    product = fields.Nested(ProductSchema, exclude=("productlines",))


class ProductImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductImage
        load_instance = True
        include_fk = True

    # Nested productline
    productline = fields.Nested(ProductLineSchema, exclude=("images",))


class SeasonEventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SeasonEvent
        load_instance = True


class AttributeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attribute
        load_instance = True


class AttributeValueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AttributeValue
        load_instance = True
        include_fk = True

    # Nested attribute
    attribute = fields.Nested(AttributeSchema, exclude=("values",))


class ProductTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductType
        load_instance = True
        include_fk = True

    # Handle self-referential parent
    parent = fields.Nested(
        lambda: ProductTypeSchema(exclude=("parent",)), allow_none=True
    )


# Many-to-many junction schemas
class Product_ProductTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product_ProductType
        load_instance = True
        include_fk = True

    product = fields.Nested(ProductSchema, exclude=("producttypes",))
    producttype = fields.Nested(ProductTypeSchema, exclude=("products",))


class ProductLine_AttributeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductLine_Attribute
        load_instance = True
        include_fk = True

    attribute = fields.Nested(AttributeSchema, exclude=("productlines",))
    productline = fields.Nested(ProductLineSchema, exclude=("attributes",))


class UserSchemaAuto(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True


# Additional schemas for collections (many=True versions)
categories_schema = CategorySchema(many=True)
products_schema = ProductSchema(many=True)
productlines_schema = ProductLineSchema(many=True)
productimage_schema = ProductImageSchema(many=True)
productimages_schema = ProductImageSchema(many=False)
seasonevents_schema = SeasonEventSchema(many=True)
attributes_schema = AttributeSchema(many=True)
attributevalues_schema = AttributeValueSchema(many=True)
producttypes_schema = ProductTypeSchema(many=True)
product_producttypes_schema = Product_ProductTypeSchema(many=True)
productline_attributes_schema = ProductLine_AttributeSchema(many=True)
product_producttypes_schema = Product_ProductTypeSchema(many=True)
productline_attributes_schema = ProductLine_AttributeSchema(many=True)
producttypes_schema = ProductTypeSchema(many=True)
product_producttypes_schema = Product_ProductTypeSchema(many=True)
productline_attributes_schema = ProductLine_AttributeSchema(many=True)
product_producttypes_schema = Product_ProductTypeSchema(many=True)
productline_attributes_schema = ProductLine_AttributeSchema(many=True)
