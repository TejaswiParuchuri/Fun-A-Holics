from fun_a_holics import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(500))
    email_id = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.username}','{self.email_id}','{self.image_file}')"
    
    def get_id(self):
           return (self.username)


class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100))
    created_by = db.Column(db.ForeignKey('users.username'), nullable=False, index=True)
    event_category = db.Column(db.String(10))
    time_created = db.Column(db.DateTime, server_default=db.FetchedValue())
    event_freq = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    cost_per_person = db.Column(db.Integer)
    link_to_connect = db.Column(db.String(50))
    max_capacity = db.Column(db.Integer)
    location = db.Column(db.String(50))
    criteria = db.Column(db.String(50))
    event_description = db.Column(db.String(500))
    event_status = db.Column(db.String(50), server_default=db.FetchedValue())
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)
    event_city = db.Column(db.String(10))
    event_state = db.Column(db.String(10))
    covid_test = db.Column(db.Integer)

    user = db.relationship('User', primaryjoin='Event.created_by == User.username', backref='events')

    def __repr__(self):
        return f"Event('{self.event_id}','{self.event_name}','{self.time_created}')"

class UserParticipation(db.Model):
    __tablename__ = 'user_participation'

    username = db.Column(db.ForeignKey('users.username'), primary_key=True, nullable=False)
    event_id = db.Column(db.ForeignKey('events.event_id'), primary_key=True, nullable=False, index=True)
    time_registered = db.Column(db.DateTime, server_default=db.FetchedValue())
    time_modified = db.Column(db.DateTime)
    joining_status = db.Column(db.String(50), server_default=db.FetchedValue())
    covid_status = db.Column(db.Integer)

    event = db.relationship('Event', primaryjoin='UserParticipation.event_id == Event.event_id', backref='user_participations')
    user = db.relationship('User', primaryjoin='UserParticipation.username == User.username', backref='user_participations')

    def __repr__(self):
        return f"User('{self.username}','{self.event_id}','{self.joining_status}')"