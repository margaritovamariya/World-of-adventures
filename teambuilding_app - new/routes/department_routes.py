from flask import Blueprint, jsonify, request, render_template
from models import Department, Category, Product
from extensions import db

department_bp = Blueprint('department', __name__)

@department_bp.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([{'id': d.id, 'name': d.name} for d in departments])

@department_bp.route('/departments', methods=['POST'])
def create_department():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Department name is required'}), 400

    department = Department(name=data['name'])
    db.session.add(department)
    db.session.commit()
    return jsonify({'id': department.id, 'name': department.name}), 201

@department_bp.route('/departments/<int:department_id>', methods=['GET'])
def show_categories(department_id):
    department = Department.query.get_or_404(department_id)
    categories = department.categories
    return render_template('categories.html', department=department, categories=categories)

# Страница за продукти в категория
@department_bp.route('/categories/<int:category_id>', methods=['GET'])
def show_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = category.products
    return render_template('products.html', category=category, products=products)