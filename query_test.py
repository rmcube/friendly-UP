import pymysql

con = pymysql.connect(host='127.0.0.1', user='root', password='4235',
                      db='study_db_test', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )
cur = con.cursor()
sql="select password from user_info"
cur.execute(sql)
result=cur.fetchall()
passwordlist=[]
for row in result:
    passwordlist.append(row['password'])
if 'asdfasdf' in passwordlist:
    print("OK")
con.commit()