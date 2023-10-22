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

    # 필수 필드 확인
    if (
        name is None
        or grade is None
        or school is None
        or password is None
        or prefer_subject is None
    ):
        return jsonify({"message": "모든 필드를 입력해야 합니다."}), 400

    # 중복된 이름 및 비밀번호 확인
    with conn.cursor() as cursor:
        query = "SELECT * FROM user WHERE name = %s AND password = %s"
        cursor.execute(query, (name, password))
        existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "중복된 이름과 비밀번호입니다. 다른 이름 또는 비밀번호를 사용해주세요."}), 400
    try:
        # 데이터베이스에 저장
        with conn.cursor() as cursor:
            query = "INSERT INTO user (name, grade, school, password, prefer_subject, created_at) VALUES (%s, %s, %s, %s, %s, NOW())"
            cursor.execute(query, (name, grade, school, password, prefer_subject))
            conn.commit()

        # with conn.cursor() as cursor:
        #     sql = "SELECT * FROM user"
        #     cursor.execute(sql)
        #     result = cursor.fetchall()
        #     print(cursor.rowcount)
        #     print(result)

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
