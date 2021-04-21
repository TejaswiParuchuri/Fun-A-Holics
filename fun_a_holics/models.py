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

class Event():
    def __init__(self, event_id, event_name, created_by, event_category, time_created, event_freq, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description , event_status, min_age, max_age , event_city , event_state , covid_test, author):
        self.event_id = event_id
        self.event_name = event_name
        self.created_by = created_by
        self.event_category = event_category
        self.time_created = time_created
        self.start_date = start_date
        self.end_date = end_date
        self.cost_per_person = cost_per_person
        self.link_to_connect = link_to_connect
        self.max_capacity = max_capacity
        self.location = location
        self.criteria = criteria
        self.event_description = event_description
        self.event_status = event_status
        self.min_age = min_age
        self.max_age = max_age
        self.event_city = event_city
        self.event_state = event_state
        self.covid_test = covid_test
        self.author = author

    def __repr__(self):
        return f"Event('{self.event_id}','{self.event_name}','{self.time_created}')"

# class User(db.Model, UserMixin):
#     age = db.Column(db.Integer)
#     username = db.Column(db.String(20), unique = True, nullable = False, primary_key=True)
#     email = db.Column(db.String(120), unique = True, nullable = False)
#     image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
#     password = db.Column(db.String(60), nullable = False)
#     events = db.relationship('Event', backref = 'author', lazy = True)

#     def __repr__(self):
#         return f"User('{self.username}','{self.email}','{self.image_file}')"

# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(100), nullable = False)
#     date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     description = db.Column(db.Text, nullable = False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)

#     def __repr__(self):
#         return f"Event('{self.title}','{self.date_added}')"
