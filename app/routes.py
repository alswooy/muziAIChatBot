# API 파일
from datetime import date , timedelta 
from flask import Blueprint, request, render_template, jsonify, Response
from flask_cors import CORS
from app.db import get_order_db, get_notice_db, get_cust_db
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


@main_bp.route('/', methods=['POST','GET'])
def index():
    bot_response = ""
    if request.method == 'POST':
        data=request.get_json()
        req=data.get('contents')
        prompt=[
            {"role": "system", "content": "너는 무지 사이트  ai야"},
            {"role": "user", "content": f"{req}"}
        ]
        res=make_prompt(prompt)
        return res

    
# 공지사항
@main_bp.route('/notice', methods=['POST'])
def notice():
    if request.method == 'POST':
        data=request.get_json()

        req=data.get('contents')
        print(req)
        day = dayfillter(req)
        contents=get_notice_db(day)
        content=makeContents(contents)
        prompt=[
            {"role": "system", "content": "너는 공지사항 요약해주기도 하고 공지사항 관련 문의를 받아주는 ai야"},
            {"role": "user", "content": f"===\n{content} \n=== {req}"}
        ]
        res=make_prompt(prompt)
        return res



#  고객
@main_bp.route('/cust',methods=['POST'])
def cust():
    if request.method == 'POST':
        data=request.get_json()
        
        # 입력을 받는다
        req=data.get('contents')
        print(f"req data: {req}")

        # 고객정보라고 입력할경우 이메일을 고객에게 요청한다
        if req in '고객정보':
            return "고객님, 고객정보를 확인하려면 이메일을 입력해주세요."

        
        try:
            # 받은입력이 문자열일경우 이메일을 , 로 분리
            if isinstance(req, str):
                req = req.split(',')
            
            # 0번째에 있는 list를 name에 저장
            # 1번째에 있는 list를 email에 저장
            email = req[0].strip()
            
            # 작성한 쿼리문에 이메일을 통해서 DB를 조회한다
            contents = get_cust_db(email)
            
            # DB조회가 된경우
            if contents:
                print(f"contents data: {contents.c_name}")
                
                prompt=[
                {"role": "system", "content": "너는 고객정보를 알려주는 AI야 너가 알려줘야할건 이름, 이메일, 전화번호, 주소뿐이야"},
                {"role": "user", "content": f"===\n{contents} \n=== {req}"}
                ]
                res=make_prompt(prompt)
                return res
            
            # DB조회가 안될경우 메시지반환
            else:
                return "죄송합니다. 입력한 정보로 조회된 고객 정보가 없습니다. 다시 확인해주세요."
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return "잘못된 입력입니다. 이름과 이메일을 다시 확인해 주세요."
    

    
    return jsonify({"error": "잘못된 요청입니다."}), 400

