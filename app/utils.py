# 유틸리티 파일
import re
import os
from openai import OpenAI
from datetime import date, timedelta

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def make_prompt(conversation):
    res = client.chat.completions.create(
        model='gpt-4o',
        messages=conversation,
        max_tokens=150,
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )
    return res.choices[0].message.content

def extract_customer_name_email(input_text):
    name_pattern = r"이름:\s*([가-힣]{2,4})"
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    name_match = re.search(name_pattern, input_text)
    email_match = re.search(email_pattern, input_text)

    name = name_match.group(1) if name_match else None
    email = email_match.group(0) if email_match else None

    print('유저정보', name, email)

    return name, email

def extract_purchase_id(input_text):
    id_pattern = r"주문\s*ID\s*:\s*(\d+)"
    match = re.search(id_pattern, input_text)
    return int(match.group(1)) if match else None

def dayfillter(input_text):
    if "삼일" in input_text:
        return (date.today()-timedelta(3)).strftime('%Y-%m-%d')
    if "3일" in input_text:
        return (date.today()-timedelta(3)).strftime('%Y-%m-%d')
    elif "일주일" in input_text:
        return (date.today()-timedelta(7)).strftime('%Y-%m-%d')
    elif "7일" in input_text:
        return (date.today()-timedelta(7)).strftime('%Y-%m-%d')
    elif "한달" in input_text:
        return (date.today()-timedelta(30)).strftime('%Y-%m-%d')
    else:
        return (date.today()-timedelta(5)).strftime('%Y-%m-%d')

def makeContents(notice):
    contents = ""
    for text in notice:
        title = text['n_title']
        content = text['n_contents']
        
        # 제목과 내용을 하나의 문자열로 이어붙임
        contents += f"제목: {title}\n내용: {content}\n\n"
    return contents


def makeOrder(order):
    contents = ""
    for text in order:
        pdtname = text['od_pdtname']
        price = text['od_price']
        date = text['od_date']
        cnt = text['od_cnt']
        print("상품명 : ", pdtname, " 가격: ", price)
        # 제목과 내용을 하나의 문자열로 이어붙임
        contents += f"상품명: {pdtname}\n 가격: {price}\n 수량 : {cnt} \n 날짜 : {date} \n"
    return contents

def makeResponse(faq):
    contents = ""
    for text in faq : 
        title = text['faq_title']
        content = text['faq_content']

        # 제목과 내용을 하나의 문자열로 이어붙임 
        contents += f"제목: {title}\n\t {content}\n"
    return contents

def generate_query_conditions(keywords):
    return " OR ".join([f"faq_title LIKE '%{keyword}%'" for keyword in keywords])