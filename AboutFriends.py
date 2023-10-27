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
        # friendID로부터 user_id 얻기
        query = "SELECT user_id FROM user WHERE friendID = %s"
        cursor.execute(query, (friend_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Friend not found."}), 404

        friend_id = result["user_id"]

        # 이미 친구인지 확인
        check_query = "SELECT * FROM friends WHERE ((user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)) AND request_status = 'friends'"
        cursor.execute(check_query, (user_id, friend_id, friend_id, user_id))
        check_result = cursor.fetchone()

        if check_result is not None:
            return jsonify({"message": "Already friends."}), 400

        # 친구 요청 상태 확인
        check_query = "SELECT * FROM friends WHERE user_id = %s AND friend_id = %s AND request_status = 'pending'"
        cursor.execute(check_query, (user_id, friend_id))
        check_result = cursor.fetchone()

        if check_result is not None:
            return jsonify({"message": "Already sent a request."}), 400

        # 친구 요청 저장
        query = "INSERT INTO friends (user_id, friend_id, request_status, created_at, updated_at) VALUES (%s, %s, 'pending', NOW(), NOW())"
        cursor.execute(query, (user_id, friend_id))
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
        query = "SELECT user_id FROM user WHERE friendID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Friend not found."}), 404

        user_id = result["user_id"]
        # 수락할 요청 찾기
        select_query = "SELECT * FROM friends WHERE friend_id = %s AND user_id = %s AND request_status = 'pending'"
        cursor.execute(select_query, (friend_id, user_id))
        result = cursor.fetchone()

        # 해당 요청이 없으면 에러 메시지 반환
        if result is None:
            return jsonify({"error": "No pending request found."}), 404

        # 수락한 요청 및 대기 중인(dummy) 데이터 삭제
        delete_query = "DELETE FROM friends WHERE (request_status = 'accepted' OR request_status = 'pending') AND ((user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s))"
        cursor.execute(delete_query, (user_id, friend_id, friend_id, user_id))
        db_conn.commit()

        # 새로운 친구 요청 상태 추가
        insert_query = "INSERT INTO friends (request_status, user_id, friend_id, created_at, updated_at) VALUES ('friends', %s, %s, NOW(), NOW())"
        cursor.execute(insert_query, (user_id, friend_id))
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
        # 수락할 요청 찾기
        query = "SELECT user_id FROM user WHERE friendID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Friend not found."}), 404

        user_id = result["user_id"]
        # 수락할 요청 찾기
        select_query = "SELECT * FROM friends WHERE friend_id = %s AND user_id = %s AND request_status = 'pending'"
        cursor.execute(select_query, (friend_id, user_id))
        result = cursor.fetchone()

        # 해당 요청이 없으면 에러 메시지 반환
        if result is None:
            return jsonify({"error": "No pending request found."}), 404

        # 수락한 요청 및 대기 중인(dummy) 데이터 삭제
        delete_query = "DELETE FROM friends WHERE (request_status = 'accepted' OR request_status = 'pending') AND ((user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s))"
        cursor.execute(delete_query, (user_id, friend_id, friend_id, user_id))
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
        # 1시간이 경과한 "pending" 상태의 요청 정보 삭제
        query = (
            "DELETE FROM friends WHERE created_at < %s AND request_status = 'pending'"
        )
        expiration_time = datetime.now() - timedelta(hours=1)
        cursor.execute(query, expiration_time)
        db_conn.commit()
    except Exception as e:
        db_conn.rollback()
    finally:
        cursor.close()
        db_conn.close()


@login_routes.route("friends_post/<int:user_id>", methods=["GET"])
def get_friendsPOST(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        check_query = (
            "SELECT * FROM friends WHERE friend_id = %s AND request_status = 'pending'"
        )
        cursor.execute(check_query, (user_id,))
        check_result = cursor.fetchall()

        if check_result is None or len(check_result) == 0:
            return jsonify({"message": "No friends found for the given user_id."}), 200

        # 조회한 유저 정보 반환
        return jsonify(check_result[0]), 200  # 리스트의 첫 번째 항목만 반환

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@login_routes.route("friends/<int:user_id>", methods=["GET"])
def get_friends(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        check_query = "SELECT * FROM friends WHERE (user_id = %s OR friend_id = %s) AND request_status = 'friends'"
        cursor.execute(check_query, (user_id, user_id))
        check_result = cursor.fetchall()

        if check_result is None or len(check_result) == 0:
            return jsonify({"message": "No friends found for the given user_id."}), 200

        # 조회한 유저 정보 반환
        return jsonify(check_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# 스케줄러 설정
scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_friend_requests, "interval", hours=1)
scheduler.start()
