
from flask import Flask,request,jsonify

app = Flask(__name__)

users = [
    {
        "user_id" : 1231231,
        "name":"solmin",
        "school":"yeonsong high school",
        "grade":3
    },
    {
        "user_id" : 13123,
        "name":"so123123lmin",
        "school":"yeonsong123123 high school",
        "grade":3
    }
]

@app.route('/users/<int:user_id>',methods=["GET"])
def get_user(user_id):
    #해당 user_id를 가진 유저 찾기
    print(user_id)
    print(type(user_id))
    
    for user in users:
        print("찾은 유저 id: ",user["user_id"])
        print("같은지 여부 : ", user["user_id"] == user_id)
        if user["user_id"] == user_id:
            return (user)
    
    # user_id가 존재하지 않을 시에 오류 메시지 반환
    return ({"error": "User not found"}), 404

@app.route('/users', methods=['GET'])
def get_users():
    name = request.args.get('name')
    grade = request.args.get('grade')
    school = request.args.get('school')
    
    filtered_users = []
    for user in users:
        if name in user['name'] and school in user['school'] and user['grade'] >= int(grade):
            filtered_users.append(user)

    return jsonify(filtered_users), 200




# 1. GET /user/{user_id}  조회 시  users 리스트에서 해당 user_id를 가진 유저 탐색해서 넘겨주기, user_id가 존재하지 않으면 오류 메세지 넘겨주기:clear!
# 2. GET /users?name={name}&grade={grade}&school={school}로 넘겨 주면
#    이름 안에 {name}이 포함되어 있고, 학교 이름 안에 {school}이 포함되어 있고, 학년이 {grade} 이상인 모든 유저 정보를 리스트로 담아서 반환하기:clear!
# 3. POST /user + body에 name, school, grade을 넘겨서 보내면 user_id, createdAt, updatedAt 필드를 추가적으로 생성하여 user 리스트 안에 추가하기
#    만약 하나의 필드라도 존재하지 않으면 오류 메세지 넘겨주기:claer!
# 4. Delete /user/{user_id} 요청 시 해당 user_id에 해당하는 데이터 삭제, user_id가 존재하지 않으면 오류 메세지 넘겨주기:clear!
# 5. PUT /user/{user_id} + body에 name, school, grade에 해당하는 정보가 담겨 있으면 해당 user_id를 가진 유저 데이터를 필드에 맞게 수정:claer?


if __name__ == '__main__':
   
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


''' 출력 깨지는거 고치기(myspl에서 flask쪽으로 정보를 가져 올경우 글씨가 깨짐,프로그램 문제로 추정)
    애들 개별 출력되도록 바꾸기
    애들 개인 코드를 0으로 시작
    뒤에 추가되되는 유저들의 숫자는 +1되도록 바꾸기 
'''