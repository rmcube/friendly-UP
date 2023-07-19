from flask import Flask, render_template
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
    cur.execute("SELECT * FROM your_table_name")
    data = cur.fetchall()

    # 데이터를 HTML 템플릿에 전달하여 웹에 출력
    return "DDDD"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
