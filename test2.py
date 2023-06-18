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
@app.route('/user', methods=['POST'])
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
            return jsonify(user), 200
    
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
