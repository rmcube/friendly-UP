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

        try:
            # pandas를 사용하여 CSV 파일 읽기
            df = pd.read_csv(csv_file_path, dtype={"학년": int, "난이도": int})

            # 열 이름을 영문으로 변경
            df = df.rename(
                columns={
                    "학교": "school",
                    "학년": "grade",
                    "난이도": "difficulty",
                    "과목": "subject",
                    "문제": "question",
                    "정답": "answer",
                    "선택1": "ans1",
                    "선택2": "ans2",
                    "선택3": "ans3",
                }
            )

            # 적재할 열 목록 정의
            columns = [
                "school",
                "grade",
                "difficulty",
                "subject",
                "question",
                "answer",
                "ans1",
                "ans2",
                "ans3",
            ]

            for _, row in df.iterrows():
                # 열 이름에 따라 데이터를 가져옵니다
                data = [row[column] for column in columns]

                query = """
                    INSERT INTO problems (school, grade, difficulty, subject,
                                          question, answer, ans1, ans2, ans3)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

                cursor.execute(
                    query,
                    tuple(data),
                )

            conn.commit()

        except pd.errors.ParserError:
            print(f"읽을 수 없는 CSV 파일: {csv_file_path}")
            continue

cursor.close()
conn.close()
