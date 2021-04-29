from fun_a_holics.models import User, Event, UserParticipation
from fun_a_holics import MailingService
from fun_a_holics import db
from sqlalchemy.sql import text

def insert_user(username, password, email_id, age):
    user = User(username = username, password = password, email_id = email_id, age = age)
    db.session.add(user)
    db.session.commit()

def select_user_email_id(email_id):
    return User.query.filter_by(email_id = email_id).first()

def select_user_username(username):
    return User.query.filter_by(username = username).first()

def update_user(age, email_id, image_file, username):
    user = User.query.filter_by(username = username).first()
    if user:
        user.age, user.email_id, user.image_file = age, email_id, image_file
    db.session.commit()
        

def insert_event(event_name, created_by, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test):
    event = Event(event_name = event_name, created_by = created_by, event_category = event_category, \
        start_date = start_date, end_date = end_date, cost_per_person = cost_per_person, link_to_connect = cost_per_person,\
        max_capacity = max_capacity, location = location, criteria = criteria, event_description = event_description, \
        min_age = min_age, max_age = max_age, event_city = event_city, event_state = event_state, covid_test = covid_test)
    db.session.add(event)
    db.session.commit()

def update_event_event_id(event_name, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test, event_id):
    event = Event.query.filter_by(event_id = event_id).first()
    if event:
        event.event_name = event_name
        event.event_category = event_category
        event.start_date = start_date
        event.end_date = end_date
        event.cost_per_person = cost_per_person
        event.link_to_connect = link_to_connect
        event.max_capacity = max_capacity
        event.location = location
        event.criteria = criteria
        event.event_description = event_description
        event.min_age = min_age
        event.max_age = max_age
        event.event_city = event_city
        event.event_state = event_state
        event.covid_test = covid_test
    db.session.commit()

def select_event_event_id(event_id):
    return Event.query.filter_by(event_id = event_id).first()

def select_all_events_event_status(event_status, per_page=None, page = None):
    if not per_page or not page:
        return Event.query.filter_by(event_status = event_status).order_by(Event.time_created.asc()).all()
    else:
        return Event.query.filter_by(event_status = event_status).order_by(Event.time_created.asc()).paginate(per_page=per_page, page = page)

def select_all_events_username(username,per_page=None, page = None):
    if not per_page or not page:
        return Event.query.filter_by(created_by = username).order_by(Event.time_created.asc()).all()
    else:
        return Event.query.filter_by(created_by = username).order_by(Event.time_created.asc()).paginate(per_page=per_page, page = page)

def cancel_event_event_id(event_id):
    event = Event.query.filter_by(event_id = event_id).first()
    if event:
        event.event_status = 'cancelled'
    db.session.commit()

def insert_user_participation(username, event_id, covid_status):
    user_participation = UserParticipation(username = username, event_id = event_id, covid_status = covid_status)
    db.session.add(user_participation)
    db.session.commit()

def delete_user_participations_event_id(event_id):
    select_user_participation_event_id(event_id)
    for user_participation in user_participations:
        db.session.delete(user_participation)
    db.session.commit()

def select_user_participation_username_event_id(username, event_id):
    return UserParticipation.query.filter_by(username = username,event_id = event_id).first()

def select_user_participation_event_id(event_id):
    return UserParticipation.query.filter_by(event_id = event_id).all()

def select_all_joined_events(username,per_page=None, page = None):
    if not per_page or not page:
        events = Event.query.join(UserParticipation, UserParticipation.event_id == Event.event_id)  \
                            .filter(UserParticipation.username == username)\
                            .order_by(Event.time_created.asc()).all()
    else:
        events = Event.query.join(UserParticipation, UserParticipation.event_id == Event.event_id)  \
                        .filter(UserParticipation.username == username)\
                        .order_by(Event.time_created.asc()).paginate(per_page=per_page, page = page)
    return events


def deregister_event_event_id(username, event_id):
    user_participation = select_user_participation_username_event_id(username, event_id)
    db.session.delete(user_participation)
    db.session.commit()

def send_mails_user(event_id):
    users = User.query.join(UserParticipation, UserParticipation.username == User.username)  \
                        .filter(UserParticipation.event_id == event_id).all()
    if users:
        to_mail=[]
        for user in users:
            to_mail.append(user.email_id)
        print(to_mail)
        event = select_event_event_id(event_id)
        if event:
            text_send="We regret to let you know that event "+ str(event.event_name)+ " is cancelled. Hence you no longer can participate"
            MailingService.send_mail(text=text_send,subject='Event Cancellation Update',to_emails=to_mail)
    return users


def send_mail_to_EO(username,event_id):
    event = select_event_event_id(event_id)
    if event:
        text_send="We want to let you know that user "+username+" has de-registered from event "+ str(event.event_name)+ "."
        MailingService.send_mail(text=text_send,subject='Participant de-registered from '+str(event.event_name)+' Update',to_emails=[event.user.email_id])

def update_events_status():
    update_query = "update events set event_status = 'inprogress' where event_id in (select temp.event_id from (select event_id from events where current_timestamp between start_date and end_date and event_status not in ('cancelled')) as temp);"
    db.engine.execute(update_query)
    update_query = "update events set event_status = 'completed' where event_id in (select temp.event_id from (select event_id from events where current_timestamp>end_date and event_status not in ('cancelled','completed')) as temp);"
    db.engine.execute(update_query)

def insert_event_cron(event_name, created_by, event_category, event_freq,start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test):
    event = Event(event_name = event_name, created_by = created_by, event_category = event_category, event_freq = event_freq,\
        start_date = start_date, end_date = end_date, cost_per_person = cost_per_person, link_to_connect = cost_per_person,\
        max_capacity = max_capacity, location = location, criteria = criteria, event_description = event_description, \
        min_age = min_age, max_age = max_age, event_city = event_city, event_state = event_state, covid_test = covid_test)
    db.session.add(event)
    db.session.commit()

def select_filter(event_category, criteria, min_age, max_age, event_status, max_capacity, event_city, event_state, cost_per_person,per_page=None, page = None):
    events_orm = Event.query
    if event_category and event_category!="select":
        events_orm = events_orm.filter_by(event_category = event_category)
    if criteria and criteria!="select":
        events_orm = events_orm.filter_by(criteria = criteria)
    events_orm = events_orm.filter(Event.min_age >= int(min_age))
    events_orm = events_orm.filter(Event.max_age <= int(max_age))
    if event_status and event_status!="select":
        events_orm = events_orm.filter_by(event_status = event_status)
    if max_capacity:
        events_orm = events_orm.filter(Event.max_capacity <= int(max_capacity))
    if event_city:
        events_orm = events_orm.filter_by(event_city = event_city)
    if event_state:
        events_orm = events_orm.filter_by(event_state = event_state)
    if cost_per_person and cost_per_person!="select":
        costs = cost_per_person.split("-")
        events_orm = events_orm.filter(Event.cost_per_person >= int(costs[0]))
        events_orm = events_orm.filter(Event.cost_per_person <= int(costs[1]))
    events = events_orm.order_by(Event.time_created.asc()).paginate(per_page=per_page, page = page)
    return events
