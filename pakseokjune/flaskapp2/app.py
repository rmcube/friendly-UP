from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Replace 'your_username', 'your_password', and 'your_database_name' with your MySQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:4235@localhost/study_db_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create a model for the 'items' table in the database
class Item(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.Integer)
    school = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Item user_id={self.user_id} grade={self.grade} school={self.school}>'

# Create the database and the required tables
db.create_all()

# Insert some sample data into the 'items' table
sample_data = [
    {'grade': 10, 'school': 'ABC High School'},
    {'grade': 12, 'school': 'XYZ High School'},
    # Add more sample data here if needed
]

for data in sample_data:
    item = Item(**data)
    db.session.add(item)

db.session.commit()
