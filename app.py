from flask import Flask, jsonify, request
import pymysql
import os
from dotenv import load_dotenv

from LoginSignup import login_routes
from query import query

load_dotenv()

app = Flask(__name__)

# MySQL 설정
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


def get_db_connection():
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db="study_db_test",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


app.register_blueprint(login_routes)


# 문제 불러오기 (차현우 임시 제작)
def random_problems(school, grade, preferred_subject):
    conn = get_db_connection()
    cursor = conn.cursor()
    selected_problems = []

    subjects = ["수학", "영어", "한국사"]

    for subject in subjects:
        if subject == preferred_subject:
            num_problems_to_select = 4
        else:
            num_problems_to_select = 1

        # problems 테이블에서 해당 과목에 해당하는 문제들을 랜덤하게 선택합니다.
        query = """
            SELECT *
            FROM problems
            WHERE school=%s AND grade=%s AND subject=%s 
            ORDER BY RAND()
            LIMIT %s
        """

        cursor.execute(query, (school, grade, subject, num_problems_to_select))

        selected_problems.extend(cursor.fetchall())

    cursor.close()

    return selected_problems


@app.route("/api/user/GET_PROBLEM", methods=["POST"])
def RETURN_PROBLEM():
    data = request.get_json()  # JSON 형식의 요청 본문을 파싱합니다.

    school = data["school"]
    grade = data["grade"]
    subject = data["subject"]

    selected_proproblems = random_problems(school, grade, subject)

    return jsonify(selected_proproblems), 200


# 정보 수정 (차현우 임시 제작)
@app.route("/api/user/inf_edit", methods=["POST"])
def inf_edit():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    data = request.get_json()
    user_id = data.get("user_id")
    school = data.get("school")
    grade = data.get("grade")
    prefer_subject = data.get("prefer_subject")
    query = """
    UPDATE user 
    SET prefer_subject=%s, grade=%s, school=%s 
    WHERE user_id=%s;
    """
    values = (prefer_subject, grade, school, user_id)

    cursor.execute(query, values)

    db_conn.commit()  # 변경 사항을 데이터베이스에 반영합니다.

    cursor.close()
    db_conn.close()
    return jsonify({"message": "Success"}), 200


# 로그인 엔드포인트
@app.route("/api/user/login", methods=["POST"])
def login():
    conn = get_db_connection()
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    # 이름과 비밀번호 확인
    if name is None or password is None:
        return jsonify({"message": "이름/비밀번호를 입력해야 합니다."}), 400

    try:
        # 데이터베이스에서 사용자 정보 조회
        query_string = query.GetUserName
        with conn.cursor() as cur:
            cur.execute(query_string, (name,))
            user = cur.fetchone()
            if str(password) == user["password"]:
                return jsonify({"message": "Success"})
            if user is None or user["password"] != str(password):
                return (
                    jsonify(
                        {
                            "message": "이름/비밀번호가 형식에 맞지 않거나 존재하지 않습니다.",
                        }
                    ),
                    400,
                )
            else:
                id_id = user["user_id"]

            # 로그인 처리
            return jsonify({"user_id": id_id}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# 특정 유저의 정보 조회
@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        # 데이터베이스 연결 및 쿼리 실행
        conn = get_db_connection()

        query_string = query.GetUser

        with conn.cursor() as cur:
            cur.execute(query_string, (user_id,))
            user = cur.fetchone()

            if user is None:
                return jsonify({"message": "해당 user_id에 해당하는 유저 정보가 없습니다."}), 404

            # 조회한 유저 정보 반환
            return jsonify(user), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        conn.close()


# 특정 유저의 상세 정보 조회
@app.route("/api/user/detail", methods=["POST"])
def get_user2():
    try:
        # 데이터베이스 연결 및 쿼리 실행
        conn = get_db_connection()
        data = request.get_json()
        user_id = data.get("user_id")
        value = data.get("value")

        if value not in [
            "name",
            "grade",
            "school",
            "password",
            "prefer_subject",
        ]:  # 유효한 필드인지 확인
            return jsonify({"message": f"Invalid field: {value}"}), 400

        query_string = (
            f"SELECT {value} FROM user WHERE user_id = %s"  # 문자열 포매팅으로 필드 이름 설정
        )
        with conn.cursor() as cur:
            cur.execute(
                query_string,
                (user_id,),  # 쉼표가 있는 튜플로 전달
            )
            user = cur.fetchone()

            if user is None:
                return jsonify({"message": "해당 user_id에 해당하는 유저 정보가 없습니다."}), 404

            # 조회한 유저 정보 반환
            return jsonify(user), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
