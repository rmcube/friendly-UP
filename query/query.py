
#정답률 (user_id, int) 
CorrectAnswerRate = "select total.b/total.a from (select count(*) as a, sum(is_correct) as b from solved where user_id = %s) as total"

#총 소요 시간 (user_id, int) 
Playtime = 'select playtime from user_info where user_id=%s'

#총 획득 재화 (user_id, int)
TotalCash = 'select total_cash from user_info where user_id=%s'

#총 진행 일수 (user_id, int)
DateSum = 'select date_sum from user_info where user_id=%s'

#친구에게 문제 보내기 횟수 (user_id, int) 
ShareSum = 'select share_sum from user_info where user_id=%s'

#친구요청 보낸 수 (user_id, int)
SendFriendSum = 'select count(*) from friends where user_id2=%s'

#친구요청 받은 수 (user_id, int)
RecieveFriendSum = 'Select count(*) from friends where user_id3=%s'

#친구 수 (user_id, int)
Friendsum = "select count(*) from friends where user_id2=%s or user_id3=%s"

#과목별 맞은 문제수(subject (text), user_id(int)), is correct==1
SolvedSumBySubject = 'select count(*) from solved where subject=%s and user_id=%s and is_correct=1'

#과목별 푼 문제수(subject(text), user_id(int))
ProblemNumBySubject = 'select count(*) from solved where subject=%s and user_id=%s'


#과목별 문제 불러오기 (subject, text)
ProblemsBySubject = 'select * from problems where subject=%s'

#cash변동 (user_id, 변동할 양)int
a=10
cash='select cash from user_info where user=%d'
cash+=a
UpdateCash = 'update user_info set cash=%d where user_id=%d'

#totalcash 증가 (user_id, 증가할 값)int
UpdateTotalCash = 'update user_info set total_cash=total_cash+%d where user_id=%s'

#datesum 증가(+1일) 전체에게
PlusDateSum = 'update user_info set date_sum=date_sum+1'

#alram 삭제(user, int)
DeleteAlarm = 'delete from alarm where user_id=%s'

#user, ALL
GetUser = "SELECT * FROM user WHERE name = %s"




'''
과목 점수 유저아이디
과학 80 2
수학 100 2
국어 80 1

{
    "과학":[
        {
            점수 : 80
            유저아이디 : 2
            푼 시간 : 30초
        },
        {
            점수 : 70
            유저아이디 : 3
            푼 시간 : 50초
        }
    ],
    "수학":[

    ],
    "국어":[

    ]

}


'''