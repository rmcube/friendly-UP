#친구요청 보낸 수 (user_id, int)
SendFriendSum = 'select count(*) from friends where user_id2=%s'

#친구요청 받은 수 (user_id, int)
RecieveFriendSum = 'Select count(*) from friends where user_id3=%s'

#친구 수
Friendsum = 'select a+b from (select count(*) as a, sum(is_correct) as b from friends)'
