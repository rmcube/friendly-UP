#문제 푼 시간,맞춘 갯수,코인 주는 값 계산 만들기 

from flask import Flask, jsonify, request, Blueprint
import pymysql
import time

app = Flask(__name__)
problem_routes = Blueprint("problem", __name__, url_prefix='/api/problem')

# MySQL 설정
db_connection = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "4235",
    "db": "study_db_test"
}

# 데이터베이스 연결 함수
def get_database_connection():
    return pymysql.connect(host=db_connection["host"],
                           user=db_connection["user"],
                           password=db_connection["password"],
                           db=db_connection["db"])

# 사용자가 푼 문제와 소요 시간을 받아 코인을 계산하여 반환
@problem_routes.route("/", methods=["POST"])
def submit_problem():
    data = request.get_json()
    user_id = data.get("user_id")
    solved_correctly = data.get("solved_correctly")
    time_taken = data.get("time_taken")

    try:
        # 데이터베이스 연결
        conn = get_database_connection()

        with conn.cursor() as cursor:
            # 사용자의 마지막 풀이 날짜 조회
            last_submission_query = "SELECT MAX(submission_date) FROM user_submissions WHERE user_id = %s"
            cursor.execute(last_submission_query, user_id)
            last_submission_date = cursor.fetchone()[0]

            # 현재 날짜를 받아옴
            current_date = time.strftime("%Y-%m-%d")

            # 마지막 풀이 날짜가 오늘인지 확인하여 이미 푼 경우 에러 반환
            if last_submission_date and last_submission_date.strftime("%Y-%m-%d") == current_date:
                return jsonify({"message": "하루에 한 번만 풀 수 있습니다."}), 400

            # 문제를 푼 시간과 맞춘 갯수를 기반으로 코인 계산
            if time_taken <= 2:
                coins_earned = 4 * solved_correctly
            elif 2 < time_taken  and time_taken <= 5:
                coins_earned = 2 * solved_correctly
            else:
                coins_earned = 1 * solved_correctly

            # 사용자의 코인을 업데이트
            update_coins_query = "UPDATE users SET coins = coins + %s WHERE user_id = %s"
            cursor.execute(update_coins_query, (coins_earned, user_id))

            # 사용자의 풀이 기록을 저장
            insert_submission_query = "INSERT INTO user_submissions (user_id, submission_date, solved_correctly, time_taken) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_submission_query, (user_id, current_date, solved_correctly, time_taken))

            # 변경사항을 커밋
            conn.commit()

            # 응답으로 코인을 반환
            response_data = {
                "coins_earned": coins_earned,
                "message": "코인이 지급되었습니다."
            }
            return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        # 연결 종료
        conn.close()

app.register_blueprint(problem_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)