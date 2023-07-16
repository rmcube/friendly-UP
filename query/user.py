from datetime import datetime


#user 정보 입력 (list) -> user정보에 저장  [name, grade, school, created_at, updated_at]    ----> create user
user = {
    "name":"solmin",
    "grade":3,
    "school":"yeonsong"
}
now=datetime.now()
now=now.strftime('%Y-%m-%d %H:%M:%S')
query = "insert into users values(%s, %s, %s, %s, %s, %s, %s)"
query.binding(none, user.get("name"), user.get("grade"), user.get("school") ,now, now)


