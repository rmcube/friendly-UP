'''문제가 학년과 학교에 맞게
초1~고3까지 영어 수학 한국사 총 36개의 분류를 만들어야한다 '예:초1 수학,고2 한국사'
유저 정보에서 (초,중,고등)학교, (1~6)학년, 선호 과목을 통해 각각의 유저의 선호 과목과 학년에 맞는 문제를 데이터베이스 안에서 랜덤으로 준다.  
즉 서버에게 데이터베이스에 학력에 맞는 문제를 보내달라하는 요청을 만들어야한다.
'''
from flask import Flask, request, jsonify
import query.query
import pymysql
import random

app = Flask(__name__)

# MySQL 데이터베이스 연결
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "4235"
app.config["MYSQL_DB"] = "study_db_test"

conn = pymysql.connect(
    host = app.config["MYSQL_HOST"], user=app.config["MYSQL_USER"], 
    db=app.config["MYSQL_DB"], password=app.config["MYSQL_PASSWORD"])

cursor = conn.cursor()

# 로그인된 유저의 정보를 기반으로 문제를 랜덤으로 제공
@app.route("/api/user/problems", methods=["GET"])
def get_user_problems():
    
    # 클라이언트에서 로그인된 유저의 정보를 전달받음
    user_info = request.get_json()

    if user_info is None: 
        return jsonify({"message": "로그인이 되어 있지 않습니다."}), 401
    
    # 로그인된 유저의 학년, 학교, 선호과목 정보 가져오기
    grade = user_info.get("grade")
    school = user_info.get("school")
    preferred_subject = user_info.get("preferred_subject")

    # 유저의 학년, 학교, 선호과목 정보를 기반으로 문제 조회
    with conn.cursor() as cursor:
        query = "SELECT * FROM problems WHERE category = %s AND subject = %s"
        # 이부분 해결해야 할 듯
        cursor.execute(query, (f"{school} {grade}", preferred_subject))
        problems = cursor.fetchall()

    # 랜덤으로 문제 선택
    selected_problem = random.choice(problems)

    # 선택한 문제 반환
    return jsonify(selected_problem), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

'''
(현재 로그인 되어 있는 유저의 정보에서 그 유저의 개인정보에 있는 학년,학교,선호과목을
읽고 이에 맞는 데이터베이스의 문제를 랜덤으로 가저온다.)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
'''