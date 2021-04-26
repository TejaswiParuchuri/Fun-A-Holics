import secrets, os
from PIL import Image
from flask import abort,render_template, url_for, flash, redirect, request
from fun_a_holics.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             EventForm,JoinEventForm)
from fun_a_holics.models import User, Event
from fun_a_holics import app, bcrypt, db, current_user
from flask_login import login_user, logout_user, login_required
from functions import *

# current_user = select_user_username('Akshay')
# current_user.is_authenticated = True
# current_user.is_active = True

@app.route('/')
@app.route('/home')
def home():
    # page = request.args.get('page', 1, type=int)
    # events = Event.query.order_by(Event.date_added.desc()).paginate(per_page=5, page = page)
    events = select_all_events_active()
    return render_template('home.html', events=events, action="created", current_user = current_user, user=None)

@app.route('/about')
def about():
    return render_template('about.html', title="About", current_user = current_user)

@app.route('/register', methods=["GET","POST"])
def register():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if validate_email(form.email.data) or validate_username(form.username.data):
            flash('Email/Username already exists!', 'danger')
            return render_template('register.html', title='Register', form=form)
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        insert_user(form.username.data, form.password.data, form.email.data, form.age.data)
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    global current_user
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = select_user_email_id(form.email.data)
        # user = User.query.filter_by(email = form.email.data).first()
        print(user)
        # if user and bcrypt.check_password_hash(user["password"],  form.password.data):
        if user and user.password==form.password.data:
        #    login_user(user_model, remember = form.remember.data)
           current_user = user
           current_user.is_authenticated = True
           current_user.is_active = True
           next_page = request.args.get('next')
           if next_page:
               return redirect(next_page)
           return redirect(url_for('home'))
        else:
           flash(f'Login Unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    # logout_user()
    global current_user
    current_user = None
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
def account():
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if (current_user.email_id!=form.email.data and validate_email(form.email.data)) or (current_user.username!=form.username.data and validate_username(form.username.data)):
            flash('Email/Username already exists!', 'danger')
            return redirect(url_for('account'))
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email_id = form.email.data
        current_user.age = form.age.data
        update_user(current_user.age, current_user.email_id,current_user.image_file,current_user.username)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':        
        form.username.data = current_user.username
        form.email.data = current_user.email_id
        form.age.data = current_user.age
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form, current_user = current_user)

@app.route('/event/new', methods = ['GET', 'POST'])
def new_event():
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = EventForm()
    if form.validate_on_submit():
        print(form)
        insert_event(form.event_name.data, current_user.username, form.event_category.data, form.start_date.data, form.end_date.data, form.cost_per_person.data, form.link_to_connect.data, form.max_capacity.data, form.location.data, form.criteria.data, form.event_description.data , form.min_age.data, form.max_age.data , form.event_city.data , form.event_state.data , form.covid_test.data)
        # event = Event(title = form.title.data, description = form.description.data, author = current_user)
        # db.session.add(event)
        # db.session.commit()
        # event_name, created_by, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description , event_status, min_age, max_age , event_city , event_state , covid_test
        flash(f'Your event has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_event.html', title='New Event', form = form, legend = 'New Event', current_user = current_user)

@app.route('/event/<int:event_id>', methods = ['GET', 'POST'])
def event(event_id):
    print('In Event ', event_id)
    join_disable = False
    if current_user:
        user_participation = select_user_participation_username_event_id(current_user.username,event_id)
        if user_participation:
            join_disable = True
    event = select_event_event_id(event_id)
    return render_template('event.html', title=event.event_name,event=event, current_user = current_user, join_disable = join_disable)

@app.route('/event/<int:event_id>/update', methods = ['GET', 'POST'])
def update_event(event_id):
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    event = select_event_event_id(event_id)
    print(event)
    if event.created_by!= current_user.username:
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        update_event_event_id(form.event_name.data, current_user.username, form.event_category.data, form.start_date.data, form.end_date.data, form.cost_per_person.data, form.link_to_connect.data, form.max_capacity.data, form.location.data, form.criteria.data, form.event_description.data , form.min_age.data, form.max_age.data , form.event_city.data , form.event_state.data , form.covid_test.data, event_id)
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
    return render_template('create_event.html', title='Update Event', current_user = current_user, event=event, form = form, legend = 'Update Event')

@app.route('/event/<int:event_id>/delete', methods = ['POST'])
def delete_event(event_id):
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    event = select_event_event_id(event_id)
    if event.created_by!= current_user.username:
        abort(403)
    cancel_event_event_id(event_id)
    flash('Your event has been cancelled!', 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_events(username):
    # page = request.args.get('page', 1, type=int)
    user = select_user_username(username)
    if not user:
        abort(403)
    events = select_all_events_username(username)
    return render_template('home.html', events=events, action="created", current_user = current_user, user=user, total = len(events))

@app.route('/event/<int:event_id>/join', methods = ['GET', 'POST'])
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

    return render_template('join_event.html', title='Join Event',event=event, current_user = current_user, form = form, legend = 'Join Event')

@app.route('/events/myevents')
def my_events():
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    username = current_user.username
    user = select_user_username(username)
    if not user:
        abort(403)
    events = select_all_events_username(username)
    return render_template('home.html', events=events, action="created", current_user = current_user, user=user, total = len(events))

@app.route('/events/events_joined')
def events_joined():
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    username = current_user.username
    user = select_user_username(username)
    if not user:
        abort(403)
    events = select_all_joined_events(username)
    return render_template('home.html', events=events,action="joined", current_user = current_user, user=user, total = len(events))

@app.route('/event/<int:event_id>/deregister', methods = ['POST'])
def deregister_event(event_id):
    if not current_user or not current_user.is_authenticated:
        return redirect(url_for('home'))
    deregister_event_event_id(current_user.username,event_id)
    flash('You have deregistered from the event!', 'success')
    return redirect(url_for('home'))