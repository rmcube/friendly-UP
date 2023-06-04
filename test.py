import pymysql
import pandas as pd

con = pymysql.connect(host='127.0.0.1', user='root', password='pq45497477',
                      db='study_db_test', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )


query='select problem_solved from user_info where user_id=="2"'

cur = con.cursor()
cur.execute(query)
con.commit()