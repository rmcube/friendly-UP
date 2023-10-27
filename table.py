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
CREATE TABLE user (
	user_id INT NOT NULL AUTO_INCREMENT ,
	name VARCHAR(50) NOT NULL,
	grade INT NOT NULL,
	school VARCHAR(50) NULL,
    friendID VARCHAR(50) NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NULL,
    shared_at DATETIME NULL,
    get_at DATETIME NULL,
	password VARCHAR(50) NOT NULL,
	cash INT NULL,
	prefer_subject VARCHAR(50) NOT NULL,
	playtime INT 	NULL,
	total_cash INT	NULL,
	date_sum INT	NULL,	
	problem_num INT	NULL,	
	problem_solved	INT	NULL,	
	share_sum	INT	NULL,	
	send_sum	INT	NULL,

	PRIMARY KEY (user_id)
);
""",
    """CREATE TABLE FriendMessage (
    id INT AUTO_INCREMENT,
    type VARCHAR(255),
    sender_id INT,
    recipient_id INT,
    problem_id INT null,
    question TEXT null,
    answer TEXT null,
    PRIMARY KEY (id)
);""",
    """
CREATE TABLE solved (
	solved_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
	user_id INT NOT NULL REFERENCES user(user_id),
	problem_id2 INT NOT NULL REFERENCES problems(problem_id),
	score INT NOT NULL, 
	time_taken TIME NOT NULL, 
	subject VARCHAR(50) DEFAULT NULL, 
	is_correct TINYINT(1) NOT NUll , 
	created_at DATETIME NOt null , 
	UPDATED_AT DATETIME NOt null 

);
""",
    """
CREATE TABLE problems (
	problem_id	INT AUTO_INCREMENT PRIMARY KEY ,
	school	VARCHAR(50)	null ,
	difficulty	int	not	null ,
    question	TEXT null ,	
    answer	TEXT null ,
	grade	int	not	null , 	
	subject	VARCHAR(50) null , 	
	ans1	TEXT null , 	
	ans2	TEXT null , 	
	ans3	TEXT NULL  	

);
""",
    """
CREATE TABLE friends (
    relation_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    request_status VARCHAR(20) NOT NULL,
    user_id INT NOT NULL REFERENCES user(user_id),
    friend_id INT NOT NULL REFERENCES user(user_id),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (friend_id) REFERENCES user(user_id)
);
""",
    """
CREATE TABLE alarm (
	ALARM_ID	int	not	null	auto_increment primary key  ,
	msg	varchar (1000)NULL   ,

	user_Id	int	not	Null	references	user(user_Id),	

	send_Id	int	not	Null	references	user(user_Id),	

	Created_At	datetime	not	null ,

	UPDATED_AT	datetime	not	null  

);

""",
]

cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS study_db_test;")
cursor.execute("CREATE DATABASE study_db_test;")
cursor.execute("USE study_db_test;")  # 추가된 구문

try:
    # 각 테이블 생성 쿼리 실행
    for query in create_table_queries:
        cursor.execute(query)

except Exception as e:
    print("Error:", str(e))

finally:
    cursor.close()
    conn.close()
