from flask import Blueprint, jsonify, request
from models import Department, Category
from extensions import db

category_bp = Blueprint('category', __name__)

@category_bp.route('/departments/<int:department_id>/categories', methods=['GET'])
def get_categories_by_department(department_id):
    department = Department.query.get_or_404(department_id)
    return jsonify([{'id': c.id, 'name': c.name} for c in department.categories])

@category_bp.route('/departments/<int:department_id>/categories', methods=['POST'])
def create_category(department_id):
    department = Department.query.get_or_404(department_id)
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Category name is required'}), 400

    category = Category(name=data['name'], department=department)
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name}), 201
