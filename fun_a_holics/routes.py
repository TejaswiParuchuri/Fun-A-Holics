import secrets, os
from PIL import Image
from flask import abort,render_template, url_for, flash, redirect, request, jsonify
from fun_a_holics.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             EventForm,JoinEventForm, FilterForm)
from fun_a_holics.models import User, Event
from fun_a_holics import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from functions import *
from db_operations import dbconnection
import datetime

@app.context_processor
def get_filter_form():
  return {"filter_form": FilterForm()}

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    events = select_all_events_event_status(event_status='active',per_page=5, page = page)
    print(events.pages)
    return render_template('home.html', events=events, action="created", user=None, next_page='home')

@app.route('/filter_events', methods=["GET","POST"])
def filter_events():
    # try:
    page = request.args.get('page', 1, type=int)
    filter_form = FilterForm()
    events = select_filter(event_category = filter_form.event_category.data,\
                                criteria = filter_form.criteria.data,\
                                min_age = filter_form.min_age.data,\
                                max_age = filter_form.max_age.data,\
                                event_status = filter_form.event_status.data,\
                                max_capacity = filter_form.max_capacity.data,\
                                event_city = filter_form.event_city.data,\
                                event_state = filter_form.event_state.data,\
                                cost_per_person = filter_form.cost_per_person.data,per_page=5, page = page)
    print(events.pages)
    return render_template('home.html', events=events, action="created", user=None, next_page='filter_events', filter_form = filter_form)
    # except Exception as e:
    #     flash('ERROR : '+str(e), 'danger')
    #     return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/register', methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if validate_email(form.email.data) or validate_username(form.username.data):
            flash('Email/Username already exists!', 'danger')
            return render_template('register.html', title='Register', form=form)
        insert_user(form.username.data, form.password.data, form.email.data, form.age.data)
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = select_user_email_id(form.email.data)
        if user and user.password==form.password.data:
           login_user(user, remember = form.remember.data)
           next_page = request.args.get('next')
           if next_page:
               return redirect(next_page)
           return redirect(url_for('home'))
        else:
           flash(f'Login unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def validate_username(username):
    user = select_user_username(username)
    if user:
        return True
    return False

def validate_email(email):
    user = select_user_email_id(email)
    if user:
        return True
    return False

@app.route('/account', methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        try:
            if (current_user.email_id!=form.email.data and validate_email(form.email.data)) or (current_user.username!=form.username.data and validate_username(form.username.data)):
                flash('Email already exists!', 'danger')
                return redirect(url_for('account'))
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.email_id = form.email.data
            current_user.age = form.age.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        except:
            flash('Cannot update account right now! Please try again later.', 'danger')
            return redirect(url_for('account'))
    elif request.method == 'GET':        
        form.username.data = current_user.username
        form.email.data = current_user.email_id
        form.age.data = current_user.age
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form)

@app.route('/event/new', methods = ['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        insert_event(form.event_name.data, current_user.username, form.event_category.data, form.start_date.data, form.end_date.data, form.cost_per_person.data, form.link_to_connect.data, form.max_capacity.data, form.location.data, form.criteria.data, form.event_description.data , form.min_age.data, form.max_age.data , form.event_city.data , form.event_state.data , form.covid_test.data)
        flash(f'Your event has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_event.html', title='New Event', form = form, legend = 'New Event')

@app.route('/event/<int:event_id>', methods = ['GET', 'POST'])
def event(event_id):
    print('In Event ', event_id)
    join_disable = False
    if current_user:
        user_participation = select_user_participation_username_event_id(current_user.username,event_id)
        if user_participation:
            join_disable = True
    event = select_event_event_id(event_id)
    user_participations = select_user_participation_event_id(event_id)
    available_slots = event.max_capacity - len(user_participations)
    return render_template('event.html', title=event.event_name,event=event, join_disable = join_disable, available_slots = available_slots)

@app.route('/event/<int:event_id>/update', methods = ['GET', 'POST'])
@login_required
def update_event(event_id):
    event = select_event_event_id(event_id)
    if event.created_by!= current_user.username:
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        update_event_event_id(form.event_name.data, form.event_category.data, form.start_date.data, form.end_date.data, form.cost_per_person.data, form.link_to_connect.data, form.max_capacity.data, form.location.data, form.criteria.data, form.event_description.data , form.min_age.data, form.max_age.data , form.event_city.data , form.event_state.data , form.covid_test.data, event_id)
        flash('Your event has been updated!', 'success')
        return redirect(url_for('event',event_id=event.event_id))
    elif request.method == 'GET':
        form.event_name.data = event.event_name
        form.event_category.data = event.event_category
        form.start_date.data = event.start_date
        form.end_date.data = event.end_date
        form.cost_per_person.data = event.cost_per_person
        form.link_to_connect.data = event.link_to_connect
        form.max_capacity.data = event.max_capacity
        form.location.data = event.location
        form.criteria.data = event.criteria
        form.event_description.data = event.event_description
        form.min_age.data = event.min_age
        form.max_age.data = event.max_age
        form.event_city.data = event.event_city
        form.event_state.data = event.event_state
        form.covid_test.data = event.covid_test
    return render_template('create_event.html', title='Update Event', event=event, form = form, legend = 'Update Event')

@app.route('/event/<int:event_id>/delete', methods = ['POST'])
@login_required
def delete_event(event_id):
    print('I am in 181')
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    event = select_event_event_id(event_id)
    if event.created_by!= current_user.username:
        abort(403)
    print('I am here')
    cancel_event_event_id(event_id)
    delete_user_participations_event_id(event_id)
    print(send_mails_user(event_id))
    flash('Your event has been cancelled!', 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_events(username):
    user = select_user_username(username)
    if not user:
        abort(403)
    page = request.args.get('page', 1, type=int)
    events = select_all_events_username(username ,per_page=5, page = page)
    return render_template('home.html', events=events, action="created", user=user, next_page='user_events')

@app.route('/event/<int:event_id>/join', methods = ['GET', 'POST'])
@login_required
def join_event(event_id):
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    event = select_event_event_id(event_id)
    print(event)
    if event.created_by== current_user.username:
        abort(403)
    form = JoinEventForm()
    # form.age.data = current_user.age
    if form.validate_on_submit():
        if current_user.age not in range(event.min_age,event.max_age+1) or form.covid_status.data!=event.covid_test:
            flash('You cannot join the '+ str(event.event_name)  +' event as you don\'t satisfy the requirements!', 'danger')
        else:
            insert_user_participation(current_user.username,event.event_id,form.covid_status.data)
            flash('Your have successfully joined the '+ str(event.event_name)  +' event!', 'success')
        return redirect(url_for('event',event_id=event.event_id))

    return render_template('join_event.html', title='Join Event',event=event, form = form, legend = 'Join Event')

@app.route('/events/myevents')
@login_required
def my_events():
    username = current_user.username
    user = select_user_username(username)
    if not user:
        abort(403)
    page = request.args.get('page', 1, type=int)
    events = select_all_events_username(username ,per_page=5, page = page)
    return render_template('home.html', events=events, action="created", user=user, next_page='my_events')

@app.route('/events/events_joined')
@login_required
def events_joined():
    username = current_user.username
    user = select_user_username(username)
    if not user:
        abort(403)
    # events = select_all_joined_events(username)
    page = request.args.get('page', 1, type=int)
    events = select_all_joined_events(username ,per_page=5, page = page)
    return render_template('home.html', events=events,action="joined", user=user, next_page='events_joined')

@app.route('/event/<int:event_id>/deregister', methods = ['POST'])
@login_required
def deregister_event(event_id):
    deregister_event_event_id(current_user.username,event_id)
    send_mail_to_EO(current_user.username,event_id)
    flash('You have deregistered from the event!', 'success')
    return redirect(url_for('home'))

@app.route('/jobsDeleteCancelled') 
def jobsDeleteCancelled():
    try:
        delete_query = "delete from user_participation where event_id in (select event_id from events where event_status in ('cancelled','completed') and end_date<=Date_sub(now(),interval 9 day));"
        db.engine.execute(delete_query)
        delete_query = "delete from events where event_status in ('cancelled','completed') and end_date<=Date_sub(now(),interval 9 day);"
        db.engine.execute(delete_query)
        return jsonify({'status':'Success'})
    except Exception as e:
        return jsonify({'status':'jobsDeleteCancelledError'+" : "+str(e)})

@app.route('/insertDailyJobs')
def insertDailyJobs():
    try:
        insert_event_cron('Pictionary','Fun-A-Holics','games','4 hours',str(datetime.date.today() + datetime.timedelta(1))+' 07:00:00',str(datetime.date.today() + datetime.timedelta(1))+' 07:30:00',"0","zoom link for online pictionary","10","zoom","indoor","Play pictionary whenever you are free","18","75","online","online","0")
        return jsonify({'status':'Success'})
    except Exception as e:
        return jsonify({'status':'insertDailyJobsError'+" : "+str(e)})

@app.route('/insertWeeklyJobs')
def insertWeeklyJobs():
    try:
        #insert_event_cron('DayTrip to Sedona','Fun-A-Holics','hiking','weekly',"concat(date_add(curdate(),interval 6 day),' 07:00:00)","concat(date_add(curdate(),interval 6 day),' 22:30:00')","80","NULL","15","sedona","outdoor","This is a day trip to Sedona devils bridge hike and other famous spots","20","50","sedona","arizona","1")
        insert_event_cron('DayTrip to Sedona','Fun-A-Holics','hiking','weekly',str(datetime.date.today() + datetime.timedelta(6))+' 07:00:00',str(datetime.date.today() + datetime.timedelta(6))+' 22:30:00',"80","NULL","15","sedona","outdoor","This is a day trip to Sedona devils bridge hike and other famous spots","20","50","sedona","arizona","1")
        #print(select_filter(None,None,'dance'))
        return jsonify({'status':'Success'})
    except Exception as e:
        return jsonify({'status':'insertWeeklyJobsError'+" : "+str(e)})

@app.route('/cronUpdateEventStatus')
def cronUpdateEventStatus():
    try:
        update_events_status()
        return jsonify({'status':'Success'})
    except Exception as e:
        return jsonify({'status':'cronUpdateEventStatusError'+" : "+str(e)})
