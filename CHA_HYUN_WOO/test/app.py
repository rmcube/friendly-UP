from flask import Flask, render_template, request
import serial

app = Flask(__name__)
ser = serial.Serial("COM3", 9600)  # 아두이노와 연결된 COM 포트와 전송 속도를 설정


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sendSignal", methods=["POST"])
def send_signal():
    ser.write(b"GOGO")
    return "Signal sent to Arduino!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
