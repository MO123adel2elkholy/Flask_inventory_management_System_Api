import uuid

from flask_login import UserMixin
from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

# Ecommerce/apps/models/inventory_models.py
from sqlalchemy.event import listens_for

from Ecommerce.apps import database as db
from Ecommerce.Email.email_handler import notify_new_product

print("inventory models Called ")


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey("category.id"), name="fk_category_parent")
    parent = db.relationship("Category", remote_side=[id], backref="children")

    def __repr__(self) -> str:
        return f"<Name: {self.name}>"


class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    pid = Column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    name = Column(String(200), unique=True, nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=False)
    is_digital = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime, server_default=db.text("CURRENT_TIMESTAMP"), onupdate=db.func.now()
    )
    category = Column(Integer, ForeignKey("category.id"))
    Stock_status = Column(String(200), default="Out_Of_Stock")
    seasonevent = Column(Integer, ForeignKey("seasonevent.id"), nullable=True)
    # Event listener: بعد إضافة المنتج مباشرة

    def __repr__(self) -> str:
        return f"<Name: {self.name}>"


class ProductLine(db.Model):
    __tablename__ = "productline"
    id = Column(Integer, primary_key=True)
    sku = Column(
        String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    price = Column(
        DECIMAL(5, 2),
    )
    stock_count = Column(Integer, default=0)
    order = Column(Integer, default=0)
    weight = Column(Float, default=0.0)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime, server_default=db.text("CURRENT_TIMESTAMP"), onupdate=db.func.now()
    )
    product_id = Column(Integer, ForeignKey("product.id"))

    def __repr__(self) -> str:
        return f"<Name: {self.sku}>"


class ProductImage(db.Model):
    __tablename__ = "productimage"
    id = Column(Integer, primary_key=True)
    alt_text = Column(String(200), unique=True, nullable=False)
    url = Column(String(200), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    order = Column(Integer)
    productline_id = Column(Integer, ForeignKey("productline.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<productImage: {self.alt_text}>"


class SeasonEvent(db.Model):
    __tablename__ = "seasonevent"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)

    def __repr__(self) -> str:
        return f"<Name: {self.name}>"


class Attribute(db.Model):
    __tablename__ = "attribute"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text)

    def __repr__(self) -> str:
        return f"<Name: {self.name}>"


class AttributeValue(db.Model):
    __tablename__ = "attributevalue"
    id = Column(Integer, primary_key=True)
    attribute_value = Column(String(200), unique=True, nullable=False)
    attribute_id = Column(Integer, ForeignKey("attribute.id"))

    def __repr__(self) -> str:
        return f"<attribute value: {self.attribute_value}>"


class ProductType(db.Model):
    __tablename__ = "producttype"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("producttype.id"))

    def __repr__(self) -> str:
        return f"<name Type: {self.name}>"


# assining Many to Many Relationship
class Product_ProductType(db.Model):
    __tablename__ = "product_producttype"
    id = Column(Integer, primary_key=True)
    producttype_id = Column(Integer, ForeignKey("producttype.id"))
    product_id = Column(Integer, ForeignKey("product.id"))


# assining Many to Many Relationship
class ProductLine_Attribute(db.Model):
    __tablename__ = "productLine_attribute"
    id = Column(Integer, primary_key=True)
    attribute_id = Column(Integer, ForeignKey("attribute.id"))
    productline_id = Column(Integer, ForeignKey("productline.id"))


class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # or password_hash
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verfied = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<User {}>".format(self.username)


@listens_for(Product, "after_insert")
def after_insert_product(mapper, connection, target):
    print("Email sent to user Now you can purches the product ")
    notify_new_product(target)


# @event.listens_for(Session, "after_commit")
# def after_commit(session):
#     for obj in session.new:
#         if isinstance(obj, Product):
#             notify_new_product(obj)
#             notify_new_product(obj)
#             notify_new_product(obj)
