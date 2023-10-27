from flask import Flask, jsonify, request, Blueprint
import pymysql
import random, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# blueprint는 메인(app.py)로 다른 파일들(class)를 묶어주는 역할을 한다
login_routes = Blueprint("member3", __name__, url_prefix="/api/user")
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


@login_routes.route("/share_solution", methods=["POST"])
def share_solution():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    sender_id = request.json["sender_id"]
    recipient_id = request.json["recipient_id"]
    question = request.json["question"]
    answer = request.json["answer"]

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

        # recipient_id에 대한 get_at 값을 가져옴
        cursor.execute("SELECT get_at FROM user WHERE user_id = %s", (recipient_id,))
        recipient_result = cursor.fetchone()

        recipient_get_at = (
            recipient_result["get_at"] if recipient_result is not None else None
        )

        # sender의 shared_at 값이 오늘 날짜와 같거나, sender의 updated_at 값이 오늘 날짜가 아니거나,
        # recipient의 get_at 값이 오늘 날짜라면 오류 메시지 반환
        if (
            sender_shared_at.date() == datetime.today().date()
            or sender_updated_at.date() != datetime.today().date()
            or (
                recipient_get_at is not None
                and recipient_get_at.date() == datetime.today().date()
            )
        ):
            return (
                jsonify(
                    {
                        "message": "하루에 두 번 보낼 수 없거나, 오늘 업데이트가 이루어지지 않았거나, 수신자가 이미 오늘 해법을 받았습니다."
                    }
                ),
                400,
            )

        query = """
        INSERT INTO FriendMessage (type, sender_id, recipient_id, question, answer)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, ("해법 공유", sender_id, recipient_id, question, answer))

        # sender의 shared_at 값을 현재 시간으로 업데이트
        cursor.execute(
            "UPDATE user SET shared_at = NOW() WHERE user_id = %s", (sender_id,)
        )

        db_conn.commit()

        return jsonify({"message": "Solution shared successfully."}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        db_conn.close()


@login_routes.route("/get_shared_solutions/<int:user_id>", methods=["GET"])
def get_shared_solutions(user_id):
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    try:
        query = """
        SELECT * FROM FriendMessage
        WHERE recipient_id = %s AND type = '해법 공유'
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
