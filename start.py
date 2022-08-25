# -*- coding: utf-8 -*-

from flask import Flask
import pandas as pd 
from sqlalchemy import create_engine
import psycopg2
engine = create_engine("postgresql://kczlivirywphmd:92be7484071849e5bdc99cde3148129fafb4c480a15b0fa66a0c2838d8ef7988@ec2-3-219-19-205.compute-1.amazonaws.com:5432/d52u3agrcchahb", echo = False)

engine.connect()

## DB 연결 
def db_create():
    
    engine.execute("""
        CREATE TABLE IF NOT EXISTS dreamspon(
            name varchar(90) NOT NULL,
            advantage varchar(10) NOT NULL,
            who varchar(40) NOT NULL,
            age int NOT NULL,
            where1 VARCHAR(30) NOT NULL,
            qualification VARCHAR(30) NOT NULL,
            url VARCHAR(70) NOT NULL,
            image VARCHAR(100) NOT NULL
        );"""
    )
    data = pd.read_csv('data/dreamspon.csv')
    print(data)
    data.to_sql(name='dreamspon', con=engine, schema = 'public', if_exists='replace', index=False)




def db_select(choice,choice1,choice2,choice3,choice4):
    #conn = psycopg2.connect(host="ec2-3-219-19-205.compute-1.amazonaws.com", dbname="d52u3agrcchahb", user="kczlivirywphmd", password="92be7484071849e5bdc99cde3148129fafb4c480a15b0fa66a0c2838d8ef7988")
    # heroku에 배포되어 있는 데이터베이스에 접속하기
    
    # choice="\'%%생활비지원%%'"
    # choice1="\'%%대학생%%'"
    # choice2=25
    # choice3="\'%%서울%%'"
    # choice4="\'%%기초수급자%%'"
    result = engine.execute("SELECT name,url,image FROM dreamspon WHERE advantage LIKE {0} AND who like {1} AND (age IS null OR age < {2}) AND (where1 IS null or where1 LIKE {3}) AND (qualification IS null or qualification LIKE {4})".format(choice,choice1,choice2,choice3,choice4))
    df = pd.DataFrame(result, columns = ['name','url', 'image'])
    # DataFrame으로 만들어주기
    # 컬럼명을 지정
    return df
                 
def area_db(naming):
# 입력된 이름이 포함된 행을 불러오는 함수

    # cursor = 임시 객체생성
    # 생성된 임시객체를 cur에 저장
    #name = "\'월성장학회 주변지역 장학'"
    result = engine.execute("SELECT name, url, image FROM dreamspon WHERE name LIKE '%%{}%%';".format(naming))
    # sql문장을 실행할 수 있게 해주는 메서드
    # name 컬럼에 naming이 포함되는 행 출력해주는 쿼리
    # 데이터내용 전부 불러서 rows에 입력
    # list 타입
    df = pd.DataFrame(result, columns = ['name', 'url', 'image'])
    #print(df)
    # DataFrame으로 만들어주기
    # 컬럼명을 지정
    return df
        
app = Flask(__name__)

@app.route("/")
def index():
    #db_create()
    return "Hello World!"


if __name__ == "__main__":
    #db_create()
    # db_select()
    # db_select1()
    app.run()

