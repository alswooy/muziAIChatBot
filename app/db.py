# DB 관련 파일
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from app.utils import generate_query_conditions
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

def get_notice_db(Date):
    engine = get_db_connections()
    query = text(f"select * from Notice where n_createDate>='{Date}'")
    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            result_list = [dict(row) for row in result.mappings()]
            return result_list
    except Exception as e:
        print(f"Failed to execute query: {e}")
        return []
    
# faq 조회 쿼리 
def get_faq_db(keyword):
    engine = get_db_connections()
    keywords = keyword.split()   # 사용자가 입력한 문장을 공백으로 구분하여 리스트로 변환

    # utils.py에 있는 SELECT * FROM faq WHERE유틸리티 함수 사용
    query_conditions = generate_query_conditions(keywords)
    query = text(f" {query_conditions}")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            result_list = [dict(row) for row in result.mappings()]
            return result_list
    except Exception as e:
        print(f"Failed to execute query: {e}")
        return []

def get_order_db(email):
    engine = get_db_connections()

    query = text("SELECT o.or_no, od.od_pdtname, o.or_prices+o.or_delvs as or_total, o.or_date FROM orders o, order_delt od WHERE o.or_no = od.or_no and o.c_email = :email AND od.od_no = (SELECT MIN(od2.od_no) FROM order_delt od2 WHERE od2.or_no = o.or_no) ORDER BY o.or_date DESC LIMIT 1;")

    if engine is None:
        return json.dumps([])
    try:
        result = execute_query(query, engine, {'email':email})
        print("db : " ,result)
        return result
    except Exception as e:
        print(f"Failed to execute query: {e}")
        return []
    
def get_orderNo(email):
    engine = get_db_connections()
    query = text("select or_no from orders where c_email= :email order by or_date DESC LIMIT 1")

    if engine is None:
        return json.dumps([])
    try:
        result = execute_query(query, engine, {'email':email})
        print("db : " ,result)
        return result
    except Exception as e:
        print(f"Failed to execute query: {e}")
        return []
    

def get_product_db():

    return []

