from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """ table name : user
        table info 
    - id : index id 
    - name 
    - start: start datetime
    - end: end datetime """
    
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    grage = db.Column(db.Integer)
    school = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, name, grade, school, created_at, updated_at):
        self.name = name
        self.grade = grade
        self.school = school
        self.created_at = created_at
        self.updated_at = updated_at