import pymysql

# MySQL 연결 정보 설정
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="4235",
    db="study_db_test",
    charset="utf8",  # 한글처리 (charset = 'utf8')
)

# 테이블 생성 쿼리문 리스트
create_table_queries = [
    """
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
""",
    """
CREATE TABLE friends (
	relation_id	INT	NOT	NULL	AUTO_INCREMENT	PRIMARY	KEY	, 
	user_id2	INT	NOT	NULL	REFERENCES	user(user_ID), 
	user_ID3	INT	NOT	NULL	REFERENCES	user(user_ID), 
	Created_at	DATETIME	NOT	NULL, 
	UPDATED_AT	DATETIME	NOT	NULL	
);

""",
    """
CREATE TABLE problems (
problem_ID	int	not	null	auto_increment primary key ,
difficulty	int	not	null ,
question	varchar(1000)	null ,
answer	varchar(1000)	null ,
subject	varchar(50)	null ,
created_at	datetime	not	null ,
updated_at	datetime	not	null 
);
""",
    """
CREATE TABLE solved (
solved_ID	int	not	null	auto_increment primary key ,	
user_ID	int	not	Null	references	user(user_ID),	
problem_Id2	int not null references problems(problem_Id),	
score	int not null , 	
time_taken	time not null , 	
subject	varchar(50)	Null , 	
is_correct	tinyint(1)	not	Null ,	
created_At	datetime not null , 	
updated_At	datetime not null 

);
""",
    """
CREATE TABLE user (
user_Id int not null auto_increment primary key ,
name varchar(50)null , 
grade int not Null,  
school varchar(50)null  ,   
password varchar(100)null  ,  
cash int Null   ,  
prefer_subject varchar(50)null   ,  
playtime time Null   ,

total_cash int Null   ,

date_sum int Null   ,

problem_num int Null   ,

problem_solved int Null   ,

share_sum int Null   ,

send_sum int Null   
);
""",
]

cursor = conn.cursor()

try:
    # 각 테이블 생성 쿼리 실행
    for query in create_table_queries:
        cursor.execute(query)

except Exception as e:
    print("Error:", str(e))

finally:
    cursor.close()
    conn.close()
