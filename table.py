import pymysql;
con = pymysql.connect(host='127.0.0.1', user='root', password='4235',
                      db='study_db_test', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )
cur = con.cursor()
sql_list = [
    '''
    CREATE TABLE `alarm` (
    `alarm_id` int NOT NULL AUTO_INCREMENT,
    `msg` varchar(1000) DEFAULT NULL,
    `user_id` int NOT NULL,
    `send_id` int NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`alarm_id`),
    KEY `user_id` (`user_id`),
    KEY `send_id` (`send_id`),
    CONSTRAINT `alarm_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
    CONSTRAINT `alarm_ibfk_2` FOREIGN KEY (`send_id`) REFERENCES `user` (`user_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    ''',
    '''
    CREATE TABLE `friends` (
    `relation_id` int NOT NULL AUTO_INCREMENT,
    `user_id2` int NOT NULL,
    `user_id3` int NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`relation_id`),
    KEY `user_id2` (`user_id2`),
    KEY `user_id3` (`user_id3`),
    CONSTRAINT `friends_ibfk_1` FOREIGN KEY (`user_id2`) REFERENCES `user` (`user_id`),
    CONSTRAINT `friends_ibfk_2` FOREIGN KEY (`user_id3`) REFERENCES `user` (`user_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    ''',
    '''
    CREATE TABLE `problems` (
    `problem_id` int NOT NULL AUTO_INCREMENT,
    `difficulty` int NOT NULL,
    `question` varchar(1000) DEFAULT NULL,
    `answer` varchar(1000) DEFAULT NULL,
    `subject` varchar(50) DEFAULT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`problem_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    ''',
    '''
    CREATE TABLE `solved` (
    `solved_id` int NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `problem_id2` int NOT NULL,
    `score` int NOT NULL,
    `time_taken` time NOT NULL,
    `subject` varchar(50) DEFAULT NULL,
    `is_correct` tinyint(1) NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`solved_id`),
    KEY `user_id` (`user_id`),
    KEY `problem_id2` (`problem_id2`),
    CONSTRAINT `solved_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
    CONSTRAINT `solved_ibfk_2` FOREIGN KEY (`problem_id2`) REFERENCES `problems` (`problem_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    ''',
    '''
    CREATE TABLE `user` (
    `user_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(50) DEFAULT NULL,
    `grade` int NOT NULL,
    `school` varchar(50) DEFAULT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`user_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    ''',
    '''
    CREATE TABLE `user_info` (
    `user_id` int NOT NULL,
    `password` varchar(100) DEFAULT NULL,
    `cash` int NOT NULL,
    `prefer_subject` varchar(50) DEFAULT NULL,
    `playtime` time NOT NULL,
    `total_cash` int NOT NULL,
    `date_sum` int NOT NULL,
    `problem_num` int NOT NULL,
    `problem_solved` int NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `send_sum` int NOT NULL,
    `share_sum` int NOT NULL,
    KEY `user_id` (`user_id`),
    CONSTRAINT `user_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    '''
]

# SQL 실행
for sql in sql_list:
    cur.execute(sql)
