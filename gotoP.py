from flask import Flask, jsonify, request, Blueprint
import pymysql
import random, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# blueprint는 메인(app.py)로 다른 파일들(class)를 묶어주는 역할을 한다
login_routes = Blueprint("member4", __name__, url_prefix="/api/user")
load_dotenv()

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


@login_routes.route("/send_problems", methods=["POST"])
def send_problems():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    sender_id = request.json["sender_id"]
    recipient_id = request.json["recipient_id"]

    try:
        # sender_id에 대한 shared_at, updated_at 값을 가져옴
        cursor.execute(
            "SELECT shared_at, updated_at FROM user WHERE user_id = %s", (sender_id,)
        )
        sender_result = cursor.fetchone()

        if sender_result is None:
            return jsonify({"message": "보내는 사람의 정보를 찾을 수 없습니다."}), 400

        sender_shared_at = sender_result["shared_at"]
        sender_updated_at = sender_result["updated_at"]

        # recipient_id에 대한 get_at, school, grade 값을 가져옴
        cursor.execute(
            "SELECT get_at, school, grade FROM user WHERE user_id = %s", (recipient_id,)
        )
        recipient_result = cursor.fetchone()

        if recipient_result is None:
            return jsonify({"message": "받는 사람의 정보를 찾을 수 없습니다."}), 400

        recipient_get_at = recipient_result["get_at"]
        school = recipient_result["school"]
        grade = recipient_result["grade"]

        # sender의 shared_at 값이 오늘 날짜일 경우 불가능
        if (
            sender_shared_at is not None
            and sender_shared_at.date() == datetime.today().date()
        ):
            return jsonify({"message": "하루에 두 번 보낼 수 없습니다."}), 400
        # sender의 updated_at 값이 오늘이 아닌 경우 불가능
        if (
            sender_updated_at is not None
            and sender_updated_at.date() != datetime.today().date()
        ):
            return jsonify({"message": "오늘 업데이트가 이루어지지 않았습니다."}), 400

        # recipient의 get_at 값이 오늘 날짜일 경우 불가능
        if (
            recipient_get_at is not None
            and recipient_get_at.date() == datetime.today().date()
        ):
            return jsonify({"message": "수신자가 이미 오늘 문제를 받았습니다."}), 400

        # 문제를 검색합니다.
        cursor.execute(
            """
            SELECT DISTINCT problem_id FROM problems
            WHERE school = %s AND grade = %s
            ORDER BY RAND()
            LIMIT 4
            """,
            (school, grade),
        )
        problem_ids = cursor.fetchall()

        # 문제가 없다면 오류 메시지를 반환합니다.
        if not problem_ids:
            return jsonify({"message": "해당 조건에 맞는 문제가 없습니다."}), 400

        # problem_ids를 리스트에 저장합니다.
        problem_ids = [problem["problem_id"] for problem in problem_ids]

        # sender의 shared_at 값을 현재 시간으로 업데이트
        cursor.execute(
            "UPDATE user SET shared_at = NOW() WHERE user_id = %s", (sender_id,)
        )

        # recipient의 get_at 값을 현재 시간으로 업데이트
        cursor.execute(
            "UPDATE user SET get_at = NOW() WHERE user_id = %s", (recipient_id,)
        )

        db_conn.commit()

        return jsonify({"problem_ids": problem_ids}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        db_conn.close()


def get_question_from_problem_id(problem_id):
    question = ""

    # MySQL 연결
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # problem_id를 사용하여 question 검색
        query = "SELECT question FROM problems WHERE problem_id = %s"
        cursor.execute(query, (problem_id,))
        result = cursor.fetchone()
        if result:
            question = result["question"]

    except Exception as e:
        print("Error:", str(e))

    finally:
        # 연결 종료
        cursor.close()
        conn.close()

    return question


@login_routes.route("/get_questions", methods=["POST"])
def api_get_questions():
    data = request.get_json()

    if "problem_ids" not in data:
        return jsonify({"error": "problem_ids is missing"}), 400

    problem_ids = data["problem_ids"]
    questions = []

    for problem_id in problem_ids:
        question = get_question_from_problem_id(problem_id)
        questions.append(question)

    return jsonify({"questions": questions}), 200


@login_routes.route("/get_pb", methods=["POST"])
def Get_PB():
    # MySQL 연결
    conn = get_db_connection()
    cursor = conn.cursor()
    question = request.json["question"]
    try:
        # question을 사용하여 problem_id 검색
        query = "SELECT problem_id FROM problems WHERE question = %s"
        cursor.execute(query, (question,))
        result = cursor.fetchone()
        if result:
            problem_id = result["problem_id"]
            return jsonify({"problem_id": problem_id})

    except Exception as e:
        print("Error:", str(e))

    finally:
        # 연결 종료
        cursor.close()
        conn.close()


@login_routes.route("/send_problem_message", methods=["POST"])
def send_problem_message():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    sender_id = request.json["sender_id"]
    recipient_id = request.json["recipient_id"]
    problem_id = request.json["problem_id"]

    try:
        # 문제 보내기 메시지를 FriendMessage 테이블에 삽입
        query = """
                INSERT INTO FriendMessage (type, sender_id, recipient_id, problem_id)
                VALUES (%s, %s, %s, %s)
                """
        cursor.execute(query, ("문제 보내기", sender_id, recipient_id, problem_id))
        db_conn.commit()

        return jsonify({"message": "문제 보내기가 완료되었습니다."}), 200

    except Exception as e:
        db_conn.rollback()
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        db_conn.close()


@login_routes.route("/get_goPB/<int:user_id>", methods=["GET"])
def get_goPB(user_id):
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    try:
        query = """
        SELECT * FROM FriendMessage
        WHERE recipient_id = %s AND type = '문제 보내기'
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        # 결과가 없다면 오류 메시지 반환
        if not results:
            return jsonify({"message": "해법 공유 메시지가 없습니다."}), 400

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        db_conn.close()


@login_routes.route("/delete_goPB/<int:recipient_id>", methods=["DELETE"])
def delete_goPB(recipient_id):
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    try:
        query = """
        DELETE FROM FriendMessage
        WHERE recipient_id = %s AND type = '문제 보내기'
        """
        cursor.execute(query, (recipient_id,))

        db_conn.commit()  # 변경 사항을 데이터베이스에 반영합니다.

        # 삭제된 row의 수를 확인합니다.
        if cursor.rowcount == 0:
            return jsonify({"message": "해당 recipient_id를 가진 해법 공유 메시지가 없습니다."}), 404
        else:
            return jsonify({"message": f"{cursor.rowcount}개의 해법 공유 메시지가 삭제되었습니다."}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        db_conn.close()
