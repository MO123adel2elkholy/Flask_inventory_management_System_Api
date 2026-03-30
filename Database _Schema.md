# Ecmomerece Mnagement system 

What the drawing is trying to convey is not one flat “products” table, it is a small
relational model that lets you keep the concepts that an e‑commerce / inventory
system has separate and connected.

If you start in the middle you will see the Product record – this is the thing a
merchant sells in the abstract. A product has the usual descriptive fields:

id – a big auto‑increment primary key.
pid – a separate identifier (SKU, GUID …) that you might expose to users.
name, slug, description, flags such as is_digital, is_active,
timestamp columns, etc.
foreign keys to category and seasonal_event (see below).
a many‑to‑many to product_type through the join table Product_ProductType
so that a given product can belong to several types (e.g. “shoe”, “men’s
apparel”, “sale item”).
The product table is not where you track stock; that is handled by the next
table.

ProductLine
A product line represents a concrete, inventory‑tracked variation of a
product – the individual SKU that you actually buy and ship. It has its own
fields:

id – PK.
price, sku (a UUID in this design), stock_qty, weight, order
(display order), is_active flag, and a type column (probably a small code or
enumeration).
product – foreign key back to the parent Product.
a many‑to‑many to AttributeValue via the join table
ProductLine_AttributeValue, which lets you attach arbitrary attributes
(colour=red, size=XL, …) to each line.
Each product line can also have zero or more ProductImage rows:

ProductImage
id – PK.
alternative_text – alt text for accessibility.
url – the location of the image file.
order – ordering of multiple pictures for the same line.
product_line – FK to the ProductLine it belongs to.
Attribute / AttributeValue / ProductLine_AttributeValue
These three tables implement a flexible attribute system.

Attribute – defines a characteristic such as “colour”, “material”,
“capacity”. It has id, name, description.

AttributeValue – stores the actual values that attributes can take. It
has id, attribute_value (e.g. “red”, “metal”, “64 GB”) and a foreign key
attribute pointing back to the Attribute definition.

ProductLine_AttributeValue – the join table (id PK, plus FKs
attribute_value and product_line) that assigns one or more values to a
particular product line.

Because the relationship is many‑to‑many you can reuse the same value across
many SKUs and you can change an attribute’s set of valid values without altering
the product‑line table.

Category
A simple hierarchical category tree:

id, name, slug, is_active flag.
parent – a self‑referencing FK so categories can be nested.
Products point at a category; you can use the slug for URL generation and the
is_active flag to hide whole branches of the catalogue.

Seasonal_Events
This table holds events such as “Black Friday”, “Christmas 2025” etc.

id, name, start_date, end_date.
Products have an optional FK to seasonal_event so you can mark them for
event‑specific pricing or display.

ProductType and Product_ProductType
Types are another way of classifying products that is orthogonal to category.

ProductType – id, name, parent (another self‑FK for type hierarchies
such as “Electronics > Mobile > Smartphones”).

Product_ProductType – join table with its own id, plus FKs product
and product_type. A product may have many types and a type may apply to
many products.

Putting it all together:

Products → categories, seasonal events, and types.
Each product has one or more product lines (the sellable SKUs).
Product lines can have images and a set of attribute‑value pairs.
Attributes and values are stored in their own tables so you can manage them
centrally and reuse them across lines.
Types and categories allow you to build navigational hierarchies and to
segment inventory for reporting.
This schema therefore separates the conceptual “what I sell” (Product) from the
concrete “what’s on my shelf” (ProductLine) and gives you flexible metadata
through attributes, images and classification tables – a typical design for an
inventory‑focused e‑commerce backend.

Raptor mini (Preview) • 1x

