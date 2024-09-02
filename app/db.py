import pymysql
from dotenv import load_dotenv
import os
import json
# 환경 변수 로드
load_dotenv()

def get_db_connection():
    """데이터베이스 연결을 생성하는 함수"""
    envhost = os.getenv('DB_HOST')
    envuser = os.getenv('DB_USER')
    envpassword = os.getenv('DB_PASSWORD')
    envdb = os.getenv('DB_NAME')

    try:
        connection = pymysql.connect(
            host=envhost, 
            user=envuser, 
            password=envpassword, 
            db=envdb, 
            charset="utf8"
        )
        print("Connection successful!")
        return connection
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None

def execute_query(query):
    """쿼리를 실행하고 결과를 반환하는 함수"""
    connection = get_db_connection()
    if connection is None:
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    finally:
        connection.close()
        print("Connection closed.")

def get_cust_db():
    query = "SELECT * FROM cust"
    return execute_query(query)

def get_notice_db():
    query = "SELECT * FROM Notice"
    return execute_query(query)

def get_faq_db():
    query = "SELECT * FROM faq"
    return execute_query(query)

def get_order_db():
    query = "SELECT * FROM orders"
    return execute_query(query)

def get_product_db():
    query = "SELECT * FROM product"
    return execute_query(query)

def get_cart_db():
    query = "SELECT * FROM cart"
    return execute_query(query)