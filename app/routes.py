# API 파일
from datetime import date , timedelta 
from flask import Blueprint, request, render_template, jsonify
from flask_cors import CORS
from app.db import get_order_db, get_notice_db
from app.utils import dayfillter, makeContents
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
        return "hi"
    if request.method == 'GET':
        print('GET HI')
        return 'hi'
    

@main_bp.route('/notice', methods=['POST'])
def notice():
    if request.method == 'POST':
        data=request.get_json()
        req=data.get('contents')
        print(req)
        day = dayfillter(req)
        contents=get_notice_db(day)
        content=makeContents(contents)
        print(content)
        prompt=[
            {"role": "system", "content": "너는 공지사항 요약해주기도 하고 공지사항 관련 문의를 받아주는 ai야"},
            {"role": "user", "content": f"===\n{contents} \n=== {req}"}
        ]
        res=make_prompt(prompt)
        return res

