from flask import Blueprint, request, jsonify
import stripe
from models import CartItem, Product


payment_bp = Blueprint('payment_bp', __name__)

# Маршрут за създаване на Stripe сесия
@payment_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Вземаме всички продукти от количката
        cart_items = CartItem.query.all()

        if not cart_items:
            return jsonify({'message': 'Cart is empty'}), 400

        # Създаваме line_items за Stripe Checkout
        line_items = []
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if not product:
                continue
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),  # Преобразуваме в центове
                },
                'quantity': item.quantity,
            })

        # Създаваме Stripe Checkout сесия
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:5000/success',
            cancel_url='http://127.0.0.1:5000/cancel',
        )
        # Връщаме URL на сесията
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400