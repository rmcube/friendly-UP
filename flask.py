import requests

url = 'http://localhost:5000/test' # POST 요청을 보낼 URL
data = {'key1': 'value1', 'key2': 'value2'} # 전송할 데이터
response = requests.post(url, json=data)

if response.status_code == 200:
    print('success')
else:
    print('error')