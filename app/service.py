import base64
import os 
import redis
import json

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
        return json({"error": "SESSION 쿠키가 없습니다."}), 400
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

