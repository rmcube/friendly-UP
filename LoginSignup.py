from flask import Flask, jsonify, request, Blueprint
import pymysql

# blueprint는 메인(app.py)로 다른 파일들(class)를 묶어주는 역할을 한다
login_routes = Blueprint("member", __name__, url_prefix="/api/user")

# MySQL 설정
db_connection = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "4235",
    "db": "study_db_test",
}

conn = pymysql.connect(
    host=db_connection["host"],
    user=db_connection["user"],
    password=db_connection["password"],
    db=db_connection["db"],
)


# 회원 가입 엔드포인트
@login_routes.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    grade = data.get("grade")
    school = data.get("school")
    password = data.get("password")
    prefer_subject = data.get("prefer_subject")

    # 필수 필드 확인
    if (
        name is None
        or grade is None
        or school is None
        or password is None
        or prefer_subject is None
    ):
        return jsonify({"message": "모든 필드를 입력해야 합니다."}), 400

    try:
        # 데이터베이스에 저장
        with conn.cursor() as cursor:
            query = "INSERT INTO user (name, grade, school, password, prefer_subject) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, grade, school, password, prefer_subject))
            conn.commit()

        # with conn.cursor() as cursor:
        #     sql = "SELECT * FROM user"
        #     cursor.execute(sql)
        #     result = cursor.fetchall()
        #     print(cursor.rowcount)
        #     print(result)
        conn = get_db_connection()
        query_string = query.GetUserName
        with conn.cursor() as cur:
            cur.execute(query_string, (name,))
            user = cur.fetchone()

            if user is None and user["password"] == str(password):
                id_id = user["user_id"]
        return jsonify({"user_id": id_id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# 로그인 엔드포인트
@login_routes.route("/api/user/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    # 이름과 비밀번호 확인
    if name is None or password is None:
        return jsonify({"message": "이름/비밀번호를 입력해야 합니다."}), 400

    try:
        # 데이터베이스에서 사용자 정보 조회
        with conn.cursor() as cursor:
            query = "SELECT * FROM user WHERE name = %s"
            cursor.execute(query, name)
            user = cursor.fetchone()

        if user is None or user["password"] != password:
            return jsonify({"message": "이름/비밀번호가 형식에 맞지 않거나 존재하지 않습니다."}), 400

        # 로그인 처리
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# 특정 유저의 정보 조회
@login_routes.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
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
