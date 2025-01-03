from app import db, app
from models import Product, Category

# Избираме категория за несвързаните продукти
default_category = Category.query.first()

# Актуализираме всички продукти без category_id
products_without_category = Product.query.filter(Product.category_id == None).all()
for product in products_without_category:
    product.category_id = default_category.id

db.session.commit()
print("All products have been assigned to a default category.")
