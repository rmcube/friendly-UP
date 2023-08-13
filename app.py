from flask import Flask, jsonify, request
import pymysql
import os
from dotenv import load_dotenv


from query import query



app = Flask(__name__)

# MySQL 설정
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="4235",
    db="study_db_test",
)

cur = conn.cursor()


app.register_blueprint(login_routes)

# 로그인 엔드포인트
@app.route("/api/user/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    # 이름과 비밀번호 확인
    if name is None or password is None:
        return jsonify({"message": "이름/비밀번호를 입력해야 합니다."}), 400

    try:
        # 데이터베이스에서 사용자 정보 조회

        query_string = query.GetUser
        with conn.cursor() as cur:
            cur.execute(query_string, (name,))
            user = cur.fetchone()

        if user is None or user["password"] != password:
            return jsonify({"message": "이름/비밀번호가 형식에 맞지 않거나 존재하지 않습니다."}), 400

        # 로그인 처리
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# 특정 유저의 정보 조회
@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        # 데이터베이스에서 특정 유저 정보 조회

        query_string = query.GetUserById
        with conn.cursor() as cur:
            cur.execute(query_string, (user_id,))
            user = cur.fetchone()

        if user is None:
            return jsonify({"message": "해당 user_id에 해당하는 유저 정보가 없습니다."}), 404

        # 조회한 유저 정보 반환
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
