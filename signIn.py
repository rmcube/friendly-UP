import pymysql
from datetime import datetime

con = pymysql.connect(host='127.0.0.1', user='root', password='4235',
                      db='study_db_test', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )
cur = con.cursor()

sql1="insert into user (name, grade, school, created_at, updated_at) values(%s, %s, %s, %s, %s)"
sql2="insert into user_info(password, cash, prefer_subject, playtime, total_cash, date_sum, problem_sum, problem_solved, created_at, updated_at, send_sum, share_sum) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

print("asdf")           
cur.execute("select password from user_info")



def sign_in(name, grade, school, password, prefer_subject):
    now=datetime.today().strftime("%Y/%m/%d %H:%M:%S") 
    cur.execute(sql1, (name, grade, school, now, now))
    cur.execute(sql2, (password, "0", prefer_subject, "0", "0", "0", "0", "0", now, now, "0", "0"))
    con.commit()


