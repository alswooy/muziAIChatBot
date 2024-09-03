# DB 관련 파일
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import json
load_dotenv()

# DB 연결
def get_db_connections():
    envhost = os.getenv('DB_HOST')
    envuser = os.getenv('DB_USER')
    envpassword = os.getenv('DB_PASSWORD')
    envdb = os.getenv('DB_NAME')
    
    try:
        engine = create_engine('mysql+pymysql://'+envuser+':'+envpassword+'@'+envhost+'/'+envdb)
        print("Connect successful!")
        return engine
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None

# JSON형식으로 변경하는 함수
def execute_query(query, engine, params=None):
    """주어진 쿼리를 실행하고 결과를 JSON 형식으로 반환하는 함수"""
    try:
        with engine.connect() as connection:
            result = connection.execute(query, params or {})
            result_list = [dict(row) for row in result.mappings()]
            return json.dumps(result_list, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"Failed to execute query: {e}")
        return json.dumps([])

# 쿼리문 작성
def get_order_db(email):
    engine = get_db_connections()
    if engine is None:
        return json.dumps([])
    # 쿼리 작성
    query = text("SELECT or_no, or_prices, or_delvs, or_date FROM orders WHERE c_email= :email")
    
    # 쿼리 실행 email이 맞는 정보만 출력
    return execute_query(query, engine, {'email': email})

def get_cust_db(email, password):
    engine = get_db_connections()
    if engine is None:
        return json.dumps([])
    # 쿼리 작성
    query = text("select ")
    
    # 쿼리 실행 email이 맞는 정보만 출력
    return execute_query(query, engine, {'email': email, 'password':password})
    