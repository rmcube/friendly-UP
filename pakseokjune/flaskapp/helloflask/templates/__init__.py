from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from user_model import User

app = Flask(__name__)

# database 설정파일
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:4235@localhost:3306/study_db_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route('/home')
def home_page():
    return render_template('home.html')
    
@app.route("/one")
def home():
	user = User.query.first()
	return 'Hello {0}, {1}, {2}, {3}, {4}'\
		.format(user.name, user.grade, user.school, user.created_at.isoformat(), user.updated_at.isoformat())
	#return render_template('home.html')
    
@app.route('/all')
def select_all():
    user = User.query.all()
    return render_template('db.html', user=user)

if __name__ == '__main__':
    app.run()
    

	