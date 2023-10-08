
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

if __name__ == '__main__':
   
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


''' 출력 깨지는거 고치기(myspl에서 flask쪽으로 정보를 가져 올경우 글씨가 깨짐,프로그램 문제로 추정)
    애들 개별 출력되도록 바꾸기
    애들 개인 코드를 0으로 시작
    뒤에 추가되되는 유저들의 숫자는 +1되도록 바꾸기 
'''