# API 파일
from datetime import date , timedelta 
from flask import Blueprint, request, render_template, jsonify
from flask_cors import CORS
from app.db import get_order_db, get_notice_db, get_cust_db, get_faq_db, get_orderNo
from app.service import redisUserID, loginPrompt, orderPrompt
from dotenv import load_dotenv
import os
from openai import OpenAI
from app.utils import (
    make_prompt,
    basicAnswer,
    matchKeyword,
    dayfillter,
    makeContents,
    makeResponse,
    makeOrder
)
load_dotenv()

main_bp = Blueprint('main', __name__)
CORS(main_bp, supports_credentials=True)
# main_bp.secret_key = os.getenv('SECRET_KEY')

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

messages = []
@main_bp.route('/test', methods=['GET'])
def test():
    response = request.cookies.get('SESSION')
    return response

@main_bp.route('/', methods=['POST'])
def index():
    bot_response = ""
    if request.method == 'POST':
        return basicAnswer(request)

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

# 문의
@main_bp.route('/faq', methods=['POST'])
def faq():
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get('contents')

        # Log user input for debugging
        print(f"FAQ 요청: {user_input}")
        
        # Fetch FAQ data based on user input
        faq_results = get_faq_db(user_input)
        formatted_faqs = makeResponse(faq_results)

        # Log FAQ results for debugging
        print(f"FAQ 결과: {formatted_faqs}")

        # Construct AI prompt for FAQ response
        prompt = [
            {"role": "system", "content": "너는 FAQ 관련 문의를 받아주는 AI야. DB를 조회해서 사용자의 질문에 답변해줘."},
            {"role": "user", "content": f"===\n{formatted_faqs}\n=== {user_input}"}
        ]

        response = make_prompt(prompt)
        return response

# 주문
@main_bp.route('/order', methods=['POST','GET'])
def order():
    userID = redisUserID(request) # service단에 redis 회원정보 구현
    
    data=request.get_json()
    user_input=data.get('contents')

    if request.method == 'POST':
        order = '주문'
        match = matchKeyword(order,user_input)
        if match == order:
            if not userID:
                return loginPrompt()
            else :
            # 주문 내역 가져오기
                return orderPrompt(userID, user_input)
        else:
            return basicAnswer(request)

        
@main_bp.route('/product', methods=['POST','GET'])
def product():
    return ""