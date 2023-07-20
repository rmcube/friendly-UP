import serial
import time

# 시리얼 포트 설정
ser = serial.Serial("COM3", 9600)

# 아두이노로 신호 전송
ser.write(b"1")  # 버튼이 눌렸음을 나타내는 신호를 보냄

# 아두이노로부터 응답 수신
while True:
    response = ser.readline().decode().strip()
    if response == "done":
        print("서보 모터 동작 완료")
        break

# 시리얼 포트 닫기
ser.close()
