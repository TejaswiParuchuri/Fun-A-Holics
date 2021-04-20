from fun_a_holics import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User():

    def __init__(self,username,email_id,password,image_file,age):
        self.is_active = None
        self.is_authenticated = None
        self.age = age
        self.username = username
        self.email_id = email_id
        self.image_file = image_file
        self.password = password

    def __repr__(self):
        return f"User('{self.username}','{self.email_id}','{self.image_file}')"

# class User(db.Model, UserMixin):
#     age = db.Column(db.Integer)
#     username = db.Column(db.String(20), unique = True, nullable = False, primary_key=True)
#     email = db.Column(db.String(120), unique = True, nullable = False)
#     image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
#     password = db.Column(db.String(60), nullable = False)
#     events = db.relationship('Event', backref = 'author', lazy = True)

#     def __repr__(self):
#         return f"User('{self.username}','{self.email}','{self.image_file}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    description = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)

    def __repr__(self):
        return f"Event('{self.title}','{self.date_added}')"
