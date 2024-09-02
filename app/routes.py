from flask import Blueprint, render_template, jsonify
from app.db import get_cust_db, get_notice_db, get_faq_db, get_order_db, get_product_db, get_cart_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    data = get_order_db()
    print(jsonify(data))
    return render_template('index.html')

@main_bp.route('/customers')
def customers():
    data = get_cust_db()

    return render_template('customers.html', data=data)

@main_bp.route('/notices')
def notices():
    data = get_notice_db()
    return render_template('notices.html', data=data)

@main_bp.route('/faqs')
def faqs():
    data = get_faq_db()
    return render_template('faqs.html', data=data)

@main_bp.route('/orders')
def orders():
    data = get_order_db()
    return render_template('orders.html', data=data)

@main_bp.route('/products')
def products():
    data = get_product_db()
    return render_template('products.html', data=data)

@main_bp.route('/cart')
def cart():
    data = get_cart_db()
    return render_template('cart.html', data=data)