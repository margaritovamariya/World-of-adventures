from extensions import db, bcrypt
from app import app
from models import Department, Category, Product

with app.app_context():
    # Добавяне на отдели
    marketing = Department(name="Marketing")
    sales = Department(name="Sales")
    db.session.add_all([marketing, sales])
    db.session.commit()

    # Добавяне на категории към отдели
    social_media = Category(name="Social Media", department=marketing)
    seo = Category(name="SEO", department=marketing)
    db.session.add_all([social_media, seo])
    db.session.commit()

    # Добавяне на продукти към категории
    product1 = Product(name="Facebook Ads", description="Advertising on Facebook", price=100.00, category=social_media)
    product2 = Product(name="Google Ads", description="Advertising on Google", price=200.00, category=seo)
    db.session.add_all([product1, product2])
    db.session.commit()
