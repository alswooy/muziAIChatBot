# API 파일
from flask import Blueprint, request
from flask_cors import CORS
from app.db import get_order_db, get_notice_db, get_faq_db, get_orderNo
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