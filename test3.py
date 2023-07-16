from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL 데이터베이스 연결
con = pymysql.connect(host='127.0.0.1', user='root', password='4235',
                      db='sgit tudy_db_test', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )

# 회원 가입 엔드포인트
@app.route('/api/user/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')
    school = data.get('school')
    password = data.get('password')
    preferred_subject = data.get('preferred_subject')

    # 필수 필드 확인
    if name is None or grade is None or school is None or password is None or preferred_subject is None:
        return jsonify({'message': '모든 필드를 입력해야 합니다.'}), 400

    try:

        return jsonify({'message': '회원 가입이 완료되었습니다.'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 로그인 엔드포인트
@app.route('/api/user/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    # 이름과 비밀번호 확인
    if name is None or password is None:
        return jsonify({'message': '이름/비밀번호를 입력해야 합니다.'}), 400

    try:
        # 데이터베이스에서 사용자 정보 조회
        with conn.cursor() as cursor:
            query = 'SELECT * FROM users WHERE name = %s'
            cursor.execute(query, name)
            user = cursor.fetchone()

        if user is None or user['password'] != password:
            return jsonify({'message': '이름/비밀번호가 형식에 맞지 않거나 존재하지 않습니다.'}), 400

        # 로그인 처리
        return jsonify({'message': 'success'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run()

'''post/api/user/singup
json data
(
    각 필드 받기
)
post/api/user/login    
json data
(
    name pw
)

만일 이름, 비번이 형식에 맞지 않을 경우
{
    "massage":'이름/비번이 형식에 맞지 않습니다.'
}
아닐 경우
{
    "massage"success"
}

회원 가입에 필요한 정보는 이름,학년,학교,비번,선호 과목을 받아야 한다.
로그인에 필요한 정보는 이름과 비번이다.(아이디를 이름이 대신한다)
'''