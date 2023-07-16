import pymysql

# MySQL 서버에 연결
conn = pymysql.connect(host='127.0.0.1', user='root', password='4235',
                      db='study_db_test', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )
cur = conn.cursor()

# user 테이블 생성 쿼리 실행
sql1 = '''
    CREATE TABLE alarm (
        alarm_id INT NOT NULL AUTO_INCREMENT,
        msg VARCHAR(1000) DEFAULT NULL,
        user_id INT NOT NULL,
        send_id INT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (alarm_id),
        KEY user_id (user_id),
        KEY send_id (send_id),
        CONSTRAINT alarm_ibfk_1 FOREIGN KEY (user_id) REFERENCES user (user_id),
        CONSTRAINT alarm_ibfk_2 FOREIGN KEY (send_id) REFERENCES user (user_id)
    ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
'''

# friends 테이블 생성 쿼리 실행
sql2 = '''
    CREATE TABLE friends (
        relation_id INT NOT NULL AUTO_INCREMENT,
        user_id2 INT NOT NULL,
        user_id3 INT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (relation_id),
        KEY user_id2 (user_id2),
        KEY user_id3 (user_id3),
        CONSTRAINT friends_ibfk_1 FOREIGN KEY (user_id2) REFERENCES user (user_id),
        CONSTRAINT friends_ibfk_2 FOREIGN KEY (user_id3) REFERENCES user (user_id)
    ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
'''

# problems 테이블 생성 쿼리 실행
sql3 = '''
    CREATE TABLE problems (
        problem_id INT NOT NULL AUTO_INCREMENT,
        difficulty INT NOT NULL,
        question VARCHAR(1000) DEFAULT NULL,
        answer VARCHAR(1000) DEFAULT NULL,
        subject VARCHAR(50) DEFAULT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (problem_id)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
'''

# solved 테이블 생성 쿼리 실행
sql4 = '''
    CREATE TABLE solved (
        solved_id INT NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL,
        problem_id2 INT NOT NULL,
        score INT NOT NULL,
        time_taken TIME NOT NULL,
        subject VARCHAR(50) DEFAULT NULL,
        is_correct TINYINT(1) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (solved_id),
        KEY user_id (user_id),
        KEY problem_id2 (problem_id2),
        CONSTRAINT solved_ibfk_1 FOREIGN KEY (user_id) REFERENCES user (user_id),
        CONSTRAINT solved_ibfk_2 FOREIGN KEY (problem_id2) REFERENCES problems (problem_id)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
'''

# user 테이블 생성 쿼리 실행
sql5 = '''
    CREATE TABLE user (
        user_id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(50) DEFAULT NULL,
        grade INT NOT NULL,
        school VARCHAR(50) DEFAULT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (user_id)
    ) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
'''

# user_info 테이블 생성 쿼리 실행
sql6 = '''
    CREATE TABLE user_info (
        user_id INT NOT NULL,
        password VARCHAR(100) DEFAULT NULL,
        cash INT NOT NULL,
        prefer_subject VARCHAR(50) DEFAULT NULL,
        playtime TIME NOT NULL,
        total_cash INT NOT NULL,
        date_sum INT NOT NULL,
        problem_num INT NOT NULL,
        problem_solved INT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        send_sum INT NOT NULL,
        share_sum INT NOT NULL,
        KEY user_id (user_id),
        CONSTRAINT user_info_ibfk_1 FOREIGN KEY (user_id) REFERENCES user (user_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
'''

# 각 테이블 생성 쿼리 실행
for sql in [sql5, sql1, sql2, sql3, sql4, sql6]:
    if cur.execute("SHOW TABLES LIKE " + "'" + sql.split()[2] + "'") == 0:
        cur.execute(sql)
        print(f"{sql.split()[2]} 테이블이 생성되었습니다.")
    else:
        print(f"{sql.split()[2]} 테이블이 이미 존재합니다.")

# 변경 내용을 커밋
conn.commit()

# 연결 해제
conn.close()