import pymysql
from dotenv import load_dotenv
import os
load_dotenv()

envhost = os.getenv('DB_HOST')
envuser = os.getenv('DB_USER')
envpassword = os.getenv('DB_PASSWORD')
envdb = os.getenv('DB_NAME')

# 데이터베이스 연결
try:
    conn = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset="utf8")
    print("Connection successful!")
except Exception as e:
    print(f"Failed to connect to the database: {e}")

curs = conn.cursor()

# 연결된 데이터베이스에서 쿼리 실행하기
curs.execute("select * from cust")

#실행된 쿼리 결과값을 가져오기
rows = curs.fetchall()

# 반복문으로 한줄씩 읽기
for row in rows:
    print(row)

# 데이터베이스 연결 종료
conn.close()