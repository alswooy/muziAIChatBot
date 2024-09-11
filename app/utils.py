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
        price = text['or_total']
        date = text['or_date']
        no = text['or_no']
        # 제목과 내용을 하나의 문자열로 이어붙임
        contents += f"주문번호 : {no} <br> 상품명: {pdtname}<br> 가격: {price} <br> 날짜 : {date} <br>"
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

def basicAnswer(request):
    data=request.get_json()
    req=data.get('contents')
    prompt=[
        {"role": "system", "content": "너는 무지 사이트  ai야"},
        {"role": "user", "content": f"{req}"}
    ]
    res=make_prompt(prompt)
    return res

def matchKeyword(keyword,user_input):
    match = re.search('주문', user_input)
    if match:
        match = match.group()
    else:
        match = ''
    return match