from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL 설정
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "4235"
app.config["MYSQL_DB"] = "study_db_test"

mysql = MySQL(app)


@app.route("/")
def index():
    # 데이터베이스 연결 및 데이터 가져오기
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    data = cur.fetchall()

    # 데이터를 JSON 형태로 변환
    json_data = []
    for row in data:
        column_names = [desc[0] for desc in cur.description]  # 열 이름 가져오기
        json_data.append(dict(zip(column_names, row)))

    # JSON 형태로 반환
    return jsonify(json_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
