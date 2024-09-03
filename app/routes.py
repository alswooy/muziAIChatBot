# API 파일
from flask import Blueprint, request, render_template, jsonify
from flask_cors import CORS
from app.db import get_order_db
from dotenv import load_dotenv
import os
from openai import OpenAI
from app.utils import (
    make_prompt, 
    extract_purchase_id,
    extract_customer_name_email
)
load_dotenv()

main_bp = Blueprint('main', __name__)
CORS(main_bp)
# main_bp.secret_key = os.getenv('SECRET_KEY')

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

messages = []

@main_bp.route('/', methods=['POST','GET'])
def index():
    bot_response = ""
    if request.method == 'POST':
        request_email=request.form.get('user_email')
        user_input = request.form.get('user_input')
        order = get_order_db(request_email)
        print('POST HI')
    if request.method == 'GET':
        print('GET HI')
    