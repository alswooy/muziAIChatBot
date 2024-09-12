import base64
import os 
import redis
import json
from app.db import get_order_db, get_orderNo
from app.utils import make_prompt, makeOrder
passwenv = os.getenv('REDIS_PASSWORD')
hostenv = os.getenv('REDIS_HOST')
portenv = os.getenv('REDIS_PORT')
redis_client = redis.StrictRedis(
    host=hostenv,  # Redis 서버 IP
    port=portenv,             # Redis 서버 포트
    db=0,                  # Redis DB 인덱스
    password=passwenv,  # Redis 서버 비밀번호
    decode_responses=True   # 응답을 문자열로 디코딩
)

def redisUserID(request) : 
    userID=""
    # Spring 서버의 /redis 엔드포인트에 GET 요청
    response = request.cookies.get('SESSION') #쿠키값 가지고오기
    if response is None:
        return json({"error": "SESSION 쿠키가 없습니다."})
    session_id = base64.b64decode(response).decode('utf-8') #
    redis_key = f"spring:session:sessions:{session_id}"
        # 해당 키의 모든 필드와 값을 가져옴 (Redis 해시 사용)
    session_data = redis_client.hgetall(redis_key)
    email_value = session_data.get("sessionAttr:c_email")
    
    if not email_value:
        userID = ""
    else:
        userID = email_value.replace('"', '')
    return userID

def loginPrompt():
    login_url = "http://localhost:8080/login"
    prompt = [
        {"role": "system", "content": f"로그인이 필요합니다. 로그인 후 다시 시도해 주세요. 회원이 로그인을 할 수 있게 링크를 알려줍니다. 클릭시 주문내역으로 이동합니다.-><a href = {login_url}>[로그인]</a>"},
        {"role": "user", "content": "로그인이 필요합니다."}
    ]
    res = make_prompt(prompt)
    return res

def orderPrompt(userID, user_input):
    contents = get_order_db(userID) # DB 정보를 빼오는 함수
    if isinstance(contents, str): # 문자열이면 json형태로 변경
        contents = json.loads(contents)
    
    content = makeOrder(contents) #DB 정보를 정리하는 함수
    prompt=[]
    no = get_orderNo(userID)
    no_list = json.loads(no)  # 문자열을 리스트로 변환

    try:
        order_no_value = no_list[0]["or_no"]
    except IndexError:
    # no_list가 비어있을 때 처리
        order_no_value = None
        print("no_list is empty.")
    except KeyError:
    # no_list[0]에 "or_no" 키가 없을 때 처리
        order_no_value = None
    print("'or_no' key not found in the first element of no_list.")

    if not order_no_value :
        prompt = [
            {"role": "system", "content": "회원의 주문내역알 알려주는 AI입니다. 주문내역이 없으니 주문을 해달라고 부탁합니다."},
            {"role": "user", "content": f"===\n{content} \n=== {user_input} "}
        ]
    else:
    # 응답 생성
        prompt = [
            {"role": "system", "content": f"회원의 주문내역을 알려주는 AI입니다. 주문내역을 출력해줍니다. 회원이 링크를 들어갈수 있게 뿌려줍니다.<a href = http://localhost:8080/orders/orderDetailList?orderNo={order_no_value}>[주문내역이동]</a>"},
            {"role": "user", "content": f"===\n{content} \n=== {user_input} "}
        ]
    res = make_prompt(prompt)
    return res