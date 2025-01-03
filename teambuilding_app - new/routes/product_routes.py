from flask import Blueprint, request, jsonify, render_template
from extensions import db
from models import Product, Category, Department

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/fix_products', methods=['POST'])
def fix_products():
    try:
        # Вземаме категорията, към която искаме да прехвърлим продуктите
        category = Category.query.filter_by(id=1, department_id=1).first()
        if not category:
            return jsonify({'error': 'Category 1 in Department 1 not found'}), 404

        # Вземаме продуктите, които все още не са свързани с категория
        products_to_update = Product.query.filter(Product.category_id == None).all()

        if not products_to_update:
            return jsonify({'message': 'No products to update'}), 200

        # Обновяваме категорията на всеки продукт
        for product in products_to_update:
            product.category_id = category.id
            db.session.add(product)  # Добавяме промените в сесията

        # Комитваме промените в базата данни
        db.session.commit()

        return jsonify({'message': f'{len(products_to_update)} products have been reassigned to Category 1 in Department 1.'}), 200
    except Exception as e:
        db.session.rollback()  # Връщаме промените при грешка
        return jsonify({'error': str(e)}), 500


@product_bp.route('/departments/<int:department_id>/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category_in_department(department_id, category_id):
    # Проверяваме дали отделът съществува
    department = Department.query.get_or_404(department_id)

    # Проверяваме дали категорията принадлежи на този отдел
    category = Category.query.filter_by(id=category_id, department_id=department.id).first_or_404()

    # Вземаме продуктите в дадената категория
    products = category.products

    # Връщаме JSON отговор с продуктите
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'recommended': product.recommended,
        'price': product.price,
        'image_url': product.image_url
    } for product in products])


# Добавяне на продукт към категория
@product_bp.route('/departments/<int:department_id>/categories/<int:category_id>/products', methods=['POST'])
def add_product_to_category_in_department(department_id, category_id):
    # Проверяваме дали отделът съществува
    department = Department.query.get_or_404(department_id)

    # Проверяваме дали категорията принадлежи на този отдел
    category = Category.query.filter_by(id=category_id, department_id=department.id).first_or_404()

    # Извличаме данните от заявката
    data = request.get_json()
    if 'name' not in data or 'description' not in data or 'price' not in data:
        return jsonify({'error': 'Name, description, and price are required fields'}), 400

    # Създаваме нов продукт
    new_product = Product(
        name=data['name'],
        description=data['description'],
        recommended = data['recommended'],
        price=data['price'],
        image_url=data.get('image_url'),
        category=category
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully', 'product': {
        'id': new_product.id,
        'name': new_product.name,
        'description': new_product.description,
        'recommended' : new_product.recommended,
        'price': new_product.price,
        'image_url': new_product.image_url
    }}), 201

# Обновяване на продукт
@product_bp.route('/products/<int:id>', methods=['PATCH'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Update only the provided fields
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'recommended' in data:
        product.recommended = data['recommended']
    if 'price' in data:
        product.price = data['price']
    if 'image_url' in data:
        product.image_url = data['image_url']

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Product updated successfully'})

# Изтриване на продукт
@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

# Рендиране на HTML страница с продукти
@product_bp.route('/products_page', methods=['GET'])
def products_page_html():
    products = Product.query.all()
    return render_template('products.html', products=products)


@product_bp.route('/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()
    products_data = [
        {"name": product.name, "description": product.description, "recommended": product.recommended, "price": product.price, "id": product.id}
        for product in products
    ]
    return jsonify(products_data)
