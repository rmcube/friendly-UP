import os
import pandas as pd
import pymysql


# MySQL 연결 정보 설정
def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="4235",
        db="study_db_test",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


conn = get_db_connection()
# 데이터를 적재할 CSV 파일 경로 지정 (경로는 실제 환경에 맞게 변경해야 합니다.)
csv_directory_path = "/home/ubuntu/friendly-UP/CSV_LIST/"

cursor = conn.cursor()

# problems 테이블 초기화
cursor.execute("TRUNCATE TABLE problems")
conn.commit()

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

        conn.commit()

cursor.close()
conn.close()