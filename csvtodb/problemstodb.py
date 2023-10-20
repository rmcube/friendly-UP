import pandas as pd
import pymysql
from sqlalchemy import create_engine


db = pymysql.connect(host="127.0.0.1", user = "root", password="4235", db = "study_db_test",charset = 'utf8')
cursor = db.cursor()


df = pd.read_csv('problems.csv',encoding = 'utf-8-sig')
df.columns = ['problem_id','difficulty', 'question', 'answer', 'subject', 'created_at', 'updated_at', 'ans1', 'ans2', 'ans3']

engine = create_engine('mysql+pymysql://root:4235@127.0.0.1/study_db_test')
conn = engine.connect()
df.to_sql(name = "problems", con = engine, if_exist = 'append', index = False)
conn.close()

sql = "select * from user limit 5"
pd.read_sql(sql,db)