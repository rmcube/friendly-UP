from flask import Flask, jsonify, request
import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime
from LoginSignup import login_routes as login_routes_signup
from AboutFriends import login_routes as login_routes_friends
from shareP import login_routes as login_routes_shareP
from gotoP import login_routes as login_routes_gotoP
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


app.register_blueprint(login_routes_signup)
app.register_blueprint(login_routes_friends)
app.register_blueprint(login_routes_shareP)
app.register_blueprint(login_routes_gotoP)


@app.route("/delete_friend", methods=["DELETE"])
def delete_friend():
    data = request.get_json()
    user_id = data.get("user_id")
    friend_id = data.get("friend_id")

    if not user_id or not friend_id:
        return jsonify({"message": "user_id and friend_id are required"}), 400

    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    try:
        # 친구 관계를 찾습니다.
        query = """
        SELECT * FROM friends
        WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)
        """
        cursor.execute(query, (user_id, friend_id, friend_id, user_id))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "No friend relationship found"}), 404

        # 찾은 친구 관계를 삭제합니다.
        query = """
        DELETE FROM friends
        WHERE relation_id = %s
        """
        cursor.execute(query, (result["relation_id"],))
        db_conn.commit()

        return jsonify({"message": "Friend deleted successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        db_conn.close()


# 문제 불러오기 (차현우 임시 제작)
def random_problems(school, grade, preferred_subject, difficulty):
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
        if difficulty != 1:
            query = """
                SELECT *
                FROM problems
                WHERE school=%s AND grade=%s AND subject=%s AND difficulty=%s
                ORDER BY RAND()
                LIMIT %s
            """

            cursor.execute(
                query, (school, grade, subject, difficulty, num_problems_to_select)
            )
        else:
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
    subject = data["prefer_subject"]
    difficulty = data["difficulty"]
    selected_proproblems = random_problems(school, grade, subject, difficulty)

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


# friendID 로 user_id 조회
@app.route("/api/user/get_user_id", methods=["POST"])
def get_user_id():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    data = request.get_json()

    friendID = data.get("friend_id")

    query = """
    SELECT user_id
    FROM user
    WHERE friendID = %s;
    """
    values = (friendID,)

    cursor.execute(query, values)
    result = cursor.fetchone()

    if result:
        user_id = result["user_id"]
        return jsonify({"user_id": user_id}), 200
    else:
        return jsonify({"message": "User not found"}), 404

    cursor.close()
    db_conn.close()


# 값 추가 ( 차현우 임시 제작 )
@app.route("/api/user/up_value", methods=["POST"])
def upValue():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    data = request.get_json()
    user_id = data.get("user_id")
    value = data.get("value")
    valueUP = data.get("valueUP")

    # Column name is inserted directly into the query using string formatting.
    # Be careful as this can make your application vulnerable to SQL Injection attacks.
    query = f"""
        UPDATE user
        SET {value} = {value} + %s
        WHERE user_id = %s;
        """

    # Only the actual values are passed to cursor.execute() method.
    values = (valueUP, user_id)

    cursor.execute(query, values)

    db_conn.commit()  # 변경 사항을 데이터베이스에 반영합니다.

    cursor.close()
    db_conn.close()

    return jsonify({"message": "Success"}), 200


# 값 다운 ( 차현우 임시 제작 )
@app.route("/api/user/up_down", methods=["POST"])
def downValue():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    data = request.get_json()
    user_id = data.get("user_id")
    value = data.get("value")
    valueUP = data.get("valueUP")

    # Column name is inserted directly into the query using string formatting.
    # Be careful as this can make your application vulnerable to SQL Injection attacks.
    query = f"""
        UPDATE user
        SET {value} = {value} - %s
        WHERE user_id = %s;
        """

    # Only the actual values are passed to cursor.execute() method.
    values = (valueUP, user_id)

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


# 업데이트 타임
@app.route("/api/user/update_time", methods=["POST"])
def update_user_time():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    data = request.get_json()

    user_id = data.get("user_id")

    # Column name is inserted directly into the query using string formatting.
    # Be careful as this can make your application vulnerable to SQL Injection attacks.
    query = f"""
        UPDATE user
        SET updated_at = %s
        WHERE user_id = %s;
        """

    # Only the actual values are passed to cursor.execute() method.
    values = (datetime.now(), user_id)

    cursor.execute(query, values)

    db_conn.commit()  # 변경 사항을 데이터베이스에 반영합니다.

    cursor.close()
    db_conn.close()

    return jsonify({"message": "Success"}), 200


@app.route("/api/user/check_update_time", methods=["POST"])
def check_update_time():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    data = request.get_json()

    user_id = data.get("user_id")

    # Get the updated_at time from the database for this user
    query_get_time = """
        SELECT updated_at
        FROM user
        WHERE user_id = %s;
        """

    cursor.execute(query_get_time, (user_id,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "No such user"}), 404

    last_updated_at_date = result["updated_at"]

    # If updated_at is NULL or the last update date is different from today's date, return "OK"
    if (
        last_updated_at_date is None
        or last_updated_at_date.date() != datetime.today().date()
    ):  # Compare dates only, not times
        message = "OK"
    else:
        message = "NO"

    # Close connection
    cursor.close()
    db_conn.close()

    return jsonify({"sign": message}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
