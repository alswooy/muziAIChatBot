from flask import Blueprint, render_template, jsonify
# from app.db import get_cust_db, get_notice_db, get_faq_db, get_order_db, get_product_db, get_cart_db
from flask_cors import CORS
from app.db import get_order_db

main_bp = Blueprint('main', __name__)
CORS(main_bp)

@main_bp.route('/')
def index():
    email = "admin@"
    data = get_order_db(email)
    print(data)
    return data