import os
import pandas as pd
import pymysql
from dotenv import load_dotenv

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


# MySQL 연결 정보 설정
def get_db_connection():
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db="study_db_test",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


# 데이터를 적재할 CSV 파일 경로 지정 (경로는 실제 환경에 맞게 변경해야 합니다.)
csv_directory_path = "/home/ubuntu/friendly-UP/CSV_LIST/"

cursor = get_db_connection.cursor()

# problems 테이블 초기화
cursor.execute("TRUNCATE TABLE problems")
get_db_connection.commit()

for filename in os.listdir(csv_directory_path):
    if filename.endswith(".csv"):
        csv_file_path = os.path.join(csv_directory_path, filename)

        # pandas를 사용하여 CSV 파일 읽기
        df = pd.read_csv(csv_file_path, dtype={"학년": int, "난이도": int})

        for i, row in df.iterrows():
            query = """
                INSERT INTO problems (school, grade, difficulty, subject,
                                      question, answer, ans1, ans2, ans3)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(
                query,
                (
                    row["학교"],
                    row["학년"],
                    row["난이도"],
                    row["과목"],
                    row["문제"],
                    row["정답"],
                    row["선택1"],
                    row["선택2"],
                    row["선택3"],
                ),
            )

        get_db_connection.commit()

cursor.close()
get_db_connection.close()
