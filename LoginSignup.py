from flask import Flask, jsonify, request, Blueprint
import pymysql
import random

# blueprint는 메인(app.py)로 다른 파일들(class)를 묶어주는 역할을 한다
login_routes = Blueprint("member2", __name__, url_prefix="/api/user")

# MySQL 설정
db_connection = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "4235",
    "db": "study_db_test",
}


def get_db_connection():
    return pymysql.connect(
        host=db_connection["host"],
        user=db_connection["user"],
        password=db_connection["password"],
        db=db_connection["db"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


# 회원 가입 엔드포인트
@login_routes.route("/signup", methods=["POST"])
def signup():
    conn = get_db_connection()
    data = request.get_json()
    name = data.get("name")
    grade = data.get("grade")
    school = data.get("school")
    password = data.get("password")
    prefer_subject = data.get("prefer_subject")

    # 중복 회원 확인
    with conn.cursor() as cursor:
        query = "SELECT * FROM user WHERE name = %s AND password = %s"
        cursor.execute(query, (name, password))
        existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "이미 존재하는 회원입니다."}), 400

    # friendID 값 생성 및 중복 확인
    while True:
        random_value = random.randrange(10000)
        friend_id = f"{name}#{random_value}"
        with conn.cursor() as cursor:
            query = "SELECT * FROM user WHERE friendID = %s"
            cursor.execute(query, (friend_id,))
            existing_friend = cursor.fetchone()
        if not existing_friend:
            break

    try:
        with conn.cursor() as cursor:
            query = """
INSERT INTO user 
(name, grade, school, friendID, created_at, password, cash, prefer_subject, playtime, 
total_cash, date_sum, problem_num, problem_solved,
share_sum,
send_sum)
VALUES (%s,%s,%s,%s,NOW(),%s,0 ,%s, 0 , 0 , 0 , 0 , 0 , 0 ,
        0)
"""

            cursor.execute(
                query, (name, grade, school, friend_id, password, prefer_subject)
            )
            conn.commit()

        return jsonify({"message": "회원 가입이 완료되었습니다."}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# 특정 유저의 정보 조회
@login_routes.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        conn = get_db_connection()
        # 데이터베이스에서 특정 유저 정보 조회
        with conn.cursor() as cursor:
            query = "SELECT * FROM user WHERE user_id = %s"
            cursor.execute(query, user_id)
            user = cursor.fetchone()

        if user is None:
            return jsonify({"message": "해당 user_id에 해당하는 유저 정보가 없습니다."}), 404

        # 조회한 유저 정보 반환
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


"""유저 정보가 만들어지면 서버에서 정보안에 보유한 캐시,플레이타임이 적히도록 추가할 것"""
