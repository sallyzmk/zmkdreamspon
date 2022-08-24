# -*- coding: utf-8 -*-

from flask import Flask
import pandas as pd
from sqlalchemy import create_engine


## DB 연결 Local
def db_create():
    #로컬
    #engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres",echo=False)
    #postgresql://username:password@localhost:5432/Maintenance database
    #Heroku
    engine = create_engine("postgresql://axliyegodnehag:9ef8dab9260e8b0c8642f9ad7dca998ccc3f53760f6ad3285310e5f0973b9c06@ec2-44-205-112-253.compute-1.amazonaws.com:5432/dcdfbmcp09gmcc", echo = False)

    engine.connect()
    engine.execute("""
        CREATE TABLE IF NOT EXISTS iris(
            sepal_length FLOAT NOT NULL,
            sepal_width FLOAT NOT NULL,
            pepal_length FLOAT NOT NULL,
            pepal_width FLOAT NOT NULL,
            species VARCHAR(100) NOT NULL
        );"""
    )
    data = pd.read_csv('data/dreamspon.csv')
    print(data)
    data.to_sql(name='dreamspon', con=engine, schema = 'public', if_exists='replace', index=False)

app = Flask(__name__)

@app.route("/")
def index():
    db_create()
    return "Hello World!"


if __name__ == "__main__":
    db_create()
    app.run()