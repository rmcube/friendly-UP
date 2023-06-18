#총 소요 시간 (user_id, int)
Playtime = 'select playtime from user_info where user_id=%s'

#총 획득 재화 (user_id, int)
TotalCash = 'select total_cash from user_info where user_id=%s'

#총 진행 일수 (user_id, int)
DateSum = 'select date_sum from user_info where user_id=%s'

#친구에게 문제 보내기 횟수 (user_id, int) 
ShareSum = 'select share_sum from user_info where user_id=%s'

#cash 감소 (user_id, 변동할 양)int
UpdateCash = 'update user_info set cash=cash+%d where user_id=%s'

#totalcash 증가 (user_id, 증가할 값)int
UpdateTotalCash = 'update user_info set total_cash=total_cash+%d where user_id=%s'

#datesum 증가(+1일) 전체에게
PlusDateSum = 'update user_info set date_sum=date_sum+1'
