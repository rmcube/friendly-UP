#맞은 문제수 (user_id, int) iscorrect가 1일때
#SolvedSum = 'select problem_solved from user_info where user_id==%s'
SolvedSum = 'select count(*) from solved where user_id==%s and is_correct==1'

#푼 문제수 (user_id, int)
#ProblemNum = 'select problem_num from user_info where user_id==%s'   
ProblemNum = 'select count(*) from solved where user_id==%s'

#정답률
CorrectAnswerRate = SolvedSum/ProblemNum

#총 소요 시간 (user_id, int)
Playtime = 'select playtime from user_info where user_id==%s'

#총 획득 재화 (user_id, int)
TotalCash = 'select total_cash from user_info where user_id==%s'

#총 진행 일수 (user_id, int)
DateSum = 'select date_sum from user_info where user_id==%s'

#친구에게 문제 보내기 횟수 (user_id, int) 
ShareSum = 'select share_sum from user_info where user_id==%s'

#친구요청 보낸 수 (user_id, int)
SendFriendSum = 'select count(*) from friends where user_id2==%s'

#친구요청 받은 수 (user_id, int)
RecieveFriendSum = 'Select count(*) from friends where user_id3==%s'


#친구 수
SendFriendSum+RecieveFriendSum

#과목별 맞은 문제수(subject (text), user_id(int)), is correct==1
SolvedSumBySubject = 'select count(*) from solved where subject==%s and user_id==%s and is_correct==1'

#과목별 푼 문제수(subject(text), user_id(int))
ProblemNumBySubject = 'select count(*) from solved where subject==%s and user_id==%s'

#과목별 정답률
CorrectAnswerRateBySubject = SolvedSumBySubject/ProblemNumBySubject

#과목별 문제 불러오기 (subject, text)
ProblemsBySubject = 'select * from problems where subject==%s'

#cash 감소 (user_id, 변동할 양)int
UpdateCash = 'update user_info set cash=cash+%d where user_id==%s'

#totalcash 증가 (user_id, 증가할 값)int
UpdateTotalCash = 'update user_info set total_cash=total_cash+%d where user_id==%s'










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