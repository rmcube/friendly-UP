from flask import Flask, jsonify, request, Blueprint
import pymysql
import random, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# blueprint는 메인(app.py)로 다른 파일들(class)를 묶어주는 역할을 한다
login_routes = Blueprint("member", __name__, url_prefix="/api/user")
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


@login_routes.route("/send_friend_request", methods=["POST"])
def send_friend_request():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    user_id = request.json["user_id"]
    friend_id = request.json["friend_id"]

    try:
        # 친구 요청 저장
        query = "INSERT INTO friends (user_id, friend_id, request_status, created_at) VALUES (%s, %s, 'pending', %s)"
        current_time = datetime.now()
        cursor.execute(query, (user_id, friend_id, current_time))
        db_conn.commit()

        return jsonify({"message": "OK"}), 200
    except Exception as e:
        db_conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db_conn.close()


@login_routes.route("/accept_friend_request", methods=["POST"])
def accept_friend_request():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    user_id = request.json["user_id"]
    friend_id = request.json["friend_id"]

    try:
        # 친구 요청 상태 업데이트
        query = "UPDATE friends SET request_status = 'accepted' WHERE user_id = %s AND friend_id = %s"
        cursor.execute(query, (friend_id, user_id))
        db_conn.commit()

        # 친구 관계 추가
        query = "INSERT INTO friends (user_id2, user_id3) VALUES (%s, %s)"
        cursor.execute(query, (user_id, friend_id))
        db_conn.commit()

        return jsonify({"message": "친구 요청을 수락했습니다."}), 200
    except Exception as e:
        db_conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db_conn.close()


@login_routes.route("/reject_friend_request", methods=["POST"])
def reject_friend_request():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    user_id = request.json["user_id"]
    friend_id = request.json["friend_id"]

    try:
        # 친구 요청 상태 업데이트
        query = "UPDATE friends SET request_status = 'rejected' WHERE user_id = %s AND friend_id = %s"
        cursor.execute(query, (friend_id, user_id))
        db_conn.commit()

        return jsonify({"message": "친구 요청을 거절했습니다."}), 200
    except Exception as e:
        db_conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db_conn.close()


def delete_expired_friend_requests():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    try:
        # 1시간이 경과한 요청 정보 삭제
        query = "DELETE FROM friends WHERE created_at < %s"
        expiration_time = datetime.now() - timedelta(hours=1)
        cursor.execute(query, expiration_time)
        db_conn.commit()
    except Exception as e:
        db_conn.rollback()
    finally:
        cursor.close()
        db_conn.close()


# 스케줄러 설정
scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_friend_requests, "interval", hours=1)
scheduler.start()