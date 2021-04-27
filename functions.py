from db_operations import dbconnection
from fun_a_holics.models import User, Event, UserParticipation
from fun_a_holics import MailingService

def insert_user(username, password, email_id, age):
    values = tuple([username, password, email_id, age])
    database = dbconnection()
    insert_query = "INSERT INTO users(username, password, email_id, age) VALUES (%s, %s, %s, %s)"
    database.insert(values,insert_query)

def select_user_email_id(email_id):
    database = dbconnection()
    login_query = "select * from users where email_id = %s limit 1"
    user = database.get_result_from_query((email_id,),login_query)
    user =  user[0] if user else None
    if user:
        user = User(user['username'],user['email_id'],user['password'],user['image_file'],user['age'])
    return user

def select_user_username(username):
    database = dbconnection()
    query = "select * from users where username = %s limit 1"
    user = database.get_result_from_query((username,),query)
    user =  user[0] if user else None
    if user:
        user = User(user['username'],user['email_id'],user['password'],user['image_file'],user['age'])
    return user

def update_user(age, email_id, image_file, username):
    values = tuple([age, email_id, image_file, username])
    database = dbconnection()
    update_query = "UPDATE users SET age=%s, email_id=%s, image_file=%s WHERE username=%s"
    database.update(values,update_query)    

def insert_event(event_name, created_by, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test):
    values = tuple([event_name, created_by, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test])
    database = dbconnection()
    insert_query = "insert into events(event_name, created_by, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    database.insert(values,insert_query)

def update_event_event_id(event_name, created_by, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test, event_id):
    values = tuple([event_name, created_by, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test, event_id])
    database = dbconnection()
    update_query = "UPDATE events SET event_name=%s, created_by=%s, event_category=%s, start_date=%s, end_date=%s, cost_per_person=%s, link_to_connect=%s, max_capacity=%s, location=%s, criteria=%s, event_description=%s, min_age=%s, max_age=%s, event_city=%s, event_state=%s, covid_test=%s WHERE event_id=%s;"
    database.update(values,update_query)

def select_event_event_id(event_id):
    database = dbconnection()
    login_query = "select * from events where event_id = %s limit 1"
    event = database.get_result_from_query((event_id,),login_query)
    event =  event[0] if event else None
    if event:
        author = select_user_username(event['created_by'])
        event = Event(event['event_id'], event['event_name'], event['created_by'], event['event_category'], event['time_created'], event['event_freq'], event['start_date'], event['end_date'], event['cost_per_person'], event['link_to_connect'], event['max_capacity'], event['location'], event['criteria'], event['event_description'] , event['event_status'], event['min_age'], event['max_age'], event['event_city'], event['event_state'], event['covid_test'], author)
    return event

def select_all_events_active():
    database = dbconnection()
    login_query = "select * from events where event_status = %s"
    events = database.get_result_from_query(('active',), login_query)
    event_objects = []
    if events:
        for event in events:
            author = select_user_username(event['created_by'])
            event = Event(event['event_id'], event['event_name'], event['created_by'], event['event_category'], event['time_created'], event['event_freq'], event['start_date'], event['end_date'], event['cost_per_person'], event['link_to_connect'], event['max_capacity'], event['location'], event['criteria'], event['event_description'] , event['event_status'], event['min_age'], event['max_age'], event['event_city'], event['event_state'], event['covid_test'], author)
            event_objects.append(event)
    return event_objects

def select_all_events_username(username):
    database = dbconnection()
    login_query = "select * from events where event_status = %s and created_by = %s"
    events = database.get_result_from_query(('active',username,), login_query)
    event_objects = []
    if events:
        for event in events:
            author = select_user_username(event['created_by'])
            event = Event(event['event_id'], event['event_name'], event['created_by'], event['event_category'], event['time_created'], event['event_freq'], event['start_date'], event['end_date'], event['cost_per_person'], event['link_to_connect'], event['max_capacity'], event['location'], event['criteria'], event['event_description'] , event['event_status'], event['min_age'], event['max_age'], event['event_city'], event['event_state'], event['covid_test'], author)
            event_objects.append(event)
    return event_objects

def cancel_event_event_id(event_id):
    database = dbconnection()
    delete_query = "update events set event_status = 'cancelled' where event_id = %s"
    database.update((event_id,),delete_query)


def insert_user_participation(username, event_id, covid_status):
    values = tuple([username, event_id, covid_status])
    database = dbconnection()
    insert_query = "INSERT INTO user_participation(username, event_id, covid_status) VALUES (%s, %s, %s)"
    database.insert(values,insert_query)

def select_user_participation_username_event_id(username, event_id):
    database = dbconnection()
    login_query = "select * from user_participation where username = %s and event_id = %s limit 1"
    user_participation = database.get_result_from_query((username,event_id,),login_query)
    user_participation =  user_participation[0] if user_participation else None
    if user_participation:
        user_participation = UserParticipation(user_participation['username'], user_participation['event_id'], user_participation['time_registered'], user_participation['time_modified'], user_participation['joining_status'], user_participation['covid_status'])
    return user_participation

def select_all_joined_events(username):
    database = dbconnection()
    login_query = "select * from events where event_status = %s  and event_id in (select event_id from user_participation where username=%s)"
    events = database.get_result_from_query(('active', username),login_query)
    event_objects = []
    if events:
        for event in events:
            author = select_user_username(event['created_by'])
            event = Event(event['event_id'], event['event_name'], event['created_by'], event['event_category'], event['time_created'], event['event_freq'], event['start_date'], event['end_date'], event['cost_per_person'], event['link_to_connect'], event['max_capacity'], event['location'], event['criteria'], event['event_description'] , event['event_status'], event['min_age'], event['max_age'], event['event_city'], event['event_state'], event['covid_test'], author)
            # print(event.event_name)
            event_objects.append(event)
    return event_objects

def deregister_event_event_id(username, event_id):
    database = dbconnection()
    delete_query = "delete from user_participation where username=%s and event_id=%s"
    database.update((username,event_id,),delete_query)

def send_mails_user(event_id):
    database = dbconnection()
    users_query = "select email_id from users where username in (select username from user_participation where event_id = %s)"
    user_names = database.get_result_from_query((event_id,), users_query)
    to_mail=[]
    if user_names:
        for mail_id in user_names:
            to_mail.append(mail_id['email_id'])
        print(to_mail)
        text_send="We regret to let you know that event "+ str(event_id)+ " is cancelled. Hence you no longer can participate"
        MailingService.send_mail(text=text_send,subject='Event Cancellation Update',to_emails=to_mail)
    return user_names

def insert_event_cron(event_name, created_by, event_category, event_freq,start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test):
    print('I am in cron')
    values = tuple([event_name, created_by, event_category, event_freq, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test])
    database = dbconnection()
    insert_query = "insert into events(event_name, created_by, event_category,event_freq, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description ,  min_age, max_age , event_city , event_state , covid_test) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    database.insert(values,insert_query)

def select_filter(age,criteria,category):
    tuples_send=()
    query="select * from events where "
    if age:
        query+=" age = %s"
        tuples_send+=(age,)
    if criteria:
        if query.endswith('where '):
            query+="criteria = %s"
        else:
            query+=" and criteria = %s"
        tuples_send+=(criteria,)
    if category:
        if query.endswith('where '):
            query+="category = %s"
        else:
            query+=" and category = %s"
        tuples_send+=(category,)
    if not query.endswith('where '):
        database = dbconnection()
        events = database.get_result_from_query(tuples_send, query)
        return events
    return 'NULL'
