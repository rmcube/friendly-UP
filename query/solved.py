#정답률 (user_id, int)
CorrectAnswerRate = "select b/a from (select count(*) as a, sum(is_correct) as b from solved where user_id = %s)"

#과목별 맞은 문제수(subject (text), user_id(int)), is correct==1
SolvedSumBySubject = 'select count(*) from solved where subject=%s and user_id=%s and is_correct=1'

#과목별 푼 문제수(subject(text), user_id(int))
ProblemNumBySubject = 'select count(*) from solved where subject=%s and user_id=%s'

#과목별 정답률
CorrectAnswerRateBySubject 