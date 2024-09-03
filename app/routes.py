# API 파일
from flask import Blueprint, request, render_template, jsonify
from flask_cors import CORS
from app.db import get_order_db
from dotenv import load_dotenv
import os
from openai import OpenAI
from utils import (
    make_prompt, 
    extract_purchase_id,
    extract_customer_name_email
)
load_dotenv()

main_bp = Blueprint('main', __name__)
CORS(main_bp)
main_bp.secret_key = os.getenv('SECRET_KEY')

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

messages = []


@main_bp.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if '구매내역' in user_input:
            email = "admin@"
            user = get_order_db(email) # DB 쿼리문 json으로 호출
        