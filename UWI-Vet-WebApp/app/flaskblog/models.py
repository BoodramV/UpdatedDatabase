from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "User "+self.username+" "+self.email+" "+self.image_file+""
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Competancy_rec(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement="auto")
    mark = db.Column(db.Boolean, nullable = True )
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comp_id = db.Column(db.Integer, db.ForeignKey('comp.id'), nullable=False)
    clinician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
   
    def __repr__(self):
        return f"Comp_rec('{self.name}')"

class Comp(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    descrip = db.Column(db.String(100))
    rot_name = db.Column(db.String(50))
    
    def __init__(self, code, rot_name="", descrip=''):
        self.id = code
        self.descrip = descrip
        self.rot_name = rot_name

    def __repr__(self):
        return f"Comp('{self.id}', '{self.descrip}', '{self.rot_name}')"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    name = db.Column(db.String(100),nullable=False)
    date_enrolled = db.Column(db.String(100),nullable=False)#(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(100),nullable=False)
    #competancy_rec = db.Column(db.Integer, db.ForeignKey('competancy_rec.id'), nullable=True)
    
    def __init__(self, id, name=' ', date_enrolled=' ', email=' '):
        self.id = id
        self.name = name
        self.date_enrolled = date_enrolled
        self.email = email
    
    def __repr__(self):
        return f"Student('{self.id}','{self.name}', '{self.date_enrolled}', '{self.email}', {self.competancy_rec}')"
