# API 파일
from flask import Blueprint, request
from flask_cors import CORS
from app.db import get_order_db, get_notice_db, get_faq_db, get_orderNo
from app.utils import dayfillter, makeContents, makeResponse, makeOrder
from app.service import redisUserID
from dotenv import load_dotenv
import os
from openai import OpenAI
from app.utils import (
    make_prompt,
    basicAnswer
)
import json
import re
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
        # 데이터가 전달되었는지 확인
        match = re.search(r'주문', user_input)
        if match:
            match = match.group()
        else:
            match = ''
        data = request.get_json()
        
        if match == '주문':
            if not userID:
                login_url = "http://localhost:8080/login"
                prompt = [
                    {"role": "system", "content": f"로그인이 필요합니다. 로그인 후 다시 시도해 주세요. 회원이 로그인을 할 수 있게 링크를 알려줍니다. 클릭시 주문내역으로 이동합니다.-><a href = {login_url}>[로그인]</a>"},
                    {"role": "user", "content": "로그인이 필요합니다."}
                ]
                res = make_prompt(prompt)
                return res
            else :
            # 주문 내역 가져오기
                contents = get_order_db(userID) # DB 정보를 빼오는 함수
                if isinstance(contents, str): # 문자열이면 json형태로 변경
                    contents = json.loads(contents)
                
                content = makeOrder(contents) #DB 정보를 정리하는 함수
                print("주문 내역: ", content)
                
                no = get_orderNo(userID)
                no_list = json.loads(no)  # 문자열을 리스트로 변환
                order_no_value = no_list[0]["or_no"]
                
                # 응답 생성
                prompt = [
                    {"role": "system", "content": f"회원의 주문내역을 알려주는 AI입니다. 주문내역을 출력해줍니다. 회원이 링크를 들어갈수 있게 뿌려줍니다.<a href = http://localhost:8080/orders/orderDetailList?orderNo={order_no_value}>[주문내역이동]</a>"},
                    {"role": "user", "content": f"===\n{content} \n=== {user_input} "}
                ]
                res = make_prompt(prompt)
                return res
        else:
            return basicAnswer(request)
        
@main_bp.route('/product', methods=['POST','GET'])
def product():

    return ""