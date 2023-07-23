'''문제가 학년과 학교에 맞게
초1~고3까지 영어 수학 한국사 총 36개의 분류를 만들어야한다 '예:초1 수학,고2 한국사'
유저 정보에서 (초,중,고등)학교, (1~6)학년, 선호 과목을 통해 각각의 유저의 선호 과목과 학년에 맞는 문제를 데이터베이스 안에서 랜덤으로 준다.  
즉 서버에게 데이터베이스에 학력에 맞는 문제를 보내달라하는 요청을 만들어야한다.
'''
from flask import Flask, request, jsonify
import pymysql
import random

app = Flask(__name__)

# MySQL 데이터베이스 연결
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "4235"
app.config["MYSQL_DB"] = "study_db_test"

conn = pymysql.connect(**app.config)
cursor = conn.cursor()

# 학력과 선호 과목을 고려하여 랜덤으로 문제 제공
@app.route("/api/problems/user", methods=["GET"])
def get_problems():
    data = request.get_json()
    school_type = data.get("school_type")
    grade = data.get("grade")
    preferred_subject = data.get("preferred_subject")

    if school_type is None or grade is None or preferred_subject is None:
        return jsonify({"message": "학교, 학년, 선호 과목 정보를 모두 입력해야 합니다."}), 400

    try:
        # 해당 학교, 학년, 선호 과목에 맞는 유저 정보 조회
        with conn.cursor() as cursor:
            query = "SELECT * FROM user WHERE school_type = %s AND grade = %s AND preferred_subject = %s"
            cursor.execute(query, (school_type, grade, preferred_subject))
            user = cursor.fetchall()

        if not user:
            return jsonify({"message": "해당 학교, 학년, 선호 과목에 맞는 유저 정보가 존재하지 않습니다."}), 404

        # 랜덤으로 유저 선택
        selected_user = random.choice(user)

        # 선택한 유저 정보를 기반으로 문제 선택
        with conn.cursor() as cursor:
            query = "SELECT * FROM problems WHERE category LIKE %s AND subject = %s"
            cursor.execute(query, (f"%{selected_user['school_type']} {selected_user['grade']}%", selected_user['preferred_subject']))
            problems = cursor.fetchall()

        if not problems:
            return jsonify({"message": "해당 학년, 학교, 선호 과목에 맞는 문제가 존재하지 않습니다."}), 404

        # 랜덤으로 문제 선택
        selected_problem = random.choice(problems)

        # 선택한 문제 반환
        return jsonify(selected_problem), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
