from flask import Flask, request, jsonify

app = Flask(__name__)

# 예시로 사용할 유저 데이터 리스트
users = [
    {
        'user_id': 1,
        'name': 'John',
        'school': 'ABC High School',
        'grade': 10,
        'createdAt': '2022-01-01',
        'updatedAt': '2022-01-01'
    },
    {
        'user_id': 2,
        'name': 'Alice',
        'school': 'XYZ Middle School',
        'grade': 9,
        'createdAt': '2022-02-01',
        'updatedAt': '2022-02-01'
    },
    {
        'user_id': 3,
        'name': 'Bob',
        'school': 'ABC High School',
        'grade': 11,
        'createdAt': '2022-03-01',
        'updatedAt': '2022-03-01'
    }
]

# 1. GET /user/{user_id}
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    print(user_id)
    for user in users:
        if user['user_id'] == user_id:
            return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# 2. GET /users?name={name}&grade={grade}&school={school}
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

# 3. POST /user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'name' not in data or 'school' not in data or 'grade' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    user = {
        'user_id': len(users) + 1,
        'name': data['name'],
        'school': data['school'],
        'grade': data['grade'],
        'createdAt': '2023-05-12',
        'updatedAt': '2023-05-12'
    }

    users.append(user)
    return jsonify(user), 201

# 4. DELETE /user/{user_id}
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['user_id'] == user_id:
            users.remove(user)
            return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404

# 5. PUT /user/{user_id}
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    for user in users:
        if user['user_id'] == user_id:
            if 'name' in data:
                user['name'] = data['name']
            if 'school' in data:
                user['school'] = data['school']
            if 'grade' in data:
                user
            if 'grade' in data:
                user['grade'] = data['grade']
            
            user['updatedAt'] = '2023-05-12'  # 업데이트된 날짜로 설정
            return jsonify(userg), 200
    
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# 1. GET /user/{user_id}  조회 시  users 리스트에서 해당 user_id를 가진 유저 탐색해서 넘겨주기, user_id가 존재하지 않으면 오류 메세지 넘겨주기:clear!
# 2. GET /users?name={name}&grade={grade}&school={school}로 넘겨 주면
#    이름 안에 {name}이 포함되어 있고, 학교 이름 안에 {school}이 포함되어 있고, 학년이 {grade} 이상인 모든 유저 정보를 리스트로 담아서 반환하기:clear!
# 3. POST /user + body에 name, school, grade을 넘겨서 보내면 user_id, createdAt, updatedAt 필드를 추가적으로 생성하여 user 리스트 안에 추가하기
#    만약 하나의 필드라도 존재하지 않으면 오류 메세지 넘겨주기:clear!
# 4. Delete /user/{user_id} 요청 시 해당 user_id에 해당하는 데이터 삭제, user_id가 존재하지 않으면 오류 메세지 넘겨주기:clear!
# 5. PUT /user/{user_id} + body에 name, school, grade에 해당하는 정보가 담겨 있으면 해당 user_id를 가진 유저 데이터를 필드에 맞게 수정/