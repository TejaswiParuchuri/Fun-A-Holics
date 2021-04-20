import secrets, os
from PIL import Image
from flask import abort,render_template, url_for, flash, redirect, request
from fun_a_holics.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             EventForm)
from fun_a_holics.models import User, Event
from fun_a_holics import app, bcrypt, db, current_user
from flask_login import login_user, logout_user, login_required
from db_operations import dbconnection

@app.route('/')
@app.route('/home')
def home():
    # page = request.args.get('page', 1, type=int)
    # events = Event.query.order_by(Event.date_added.desc()).paginate(per_page=5, page = page)
    events = None
    return render_template('home.html', events=events, current_user = current_user)

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
        database = dbconnection()
        insert_query = "INSERT INTO users(username, password, email_id, age) VALUES (%s, %s, %s, %s)"
        database.insert((form.username.data, form.password.data, form.email.data, form.age.data),insert_query)
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
        database = dbconnection()
        login_query = "select * from users where email_id = %s"
        user = database.get_result_from_query((form.email.data,),login_query)
        # user = User.query.filter_by(email = form.email.data).first()
        print(user)
        # if user and bcrypt.check_password_hash(user[0]["password"],  form.password.data):
        if user and user[0]["password"]==form.password.data:
           user_model = User(username = user[0]["username"], email_id = user[0]["email_id"], password = user[0]["password"], image_file = user[0]["image_file"], age = user[0]["age"])
           login_user(user_model, remember = form.remember.data)
           current_user = user_model
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
    database = dbconnection()
    query = "select * from users where username = %s"
    user = database.get_result_from_query((username,),query)
    if len(user)>0:
        return True
    return False

def validate_email(email):
    database = dbconnection()
    query = "select * from users where email_id = %s"
    user = database.get_result_from_query((email,),query)
    if len(user)>0:
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
        # db.session.commit()
        database = dbconnection()
        update_query = "UPDATE users SET age=%s, email_id=%s, image_file=%s WHERE username=%s"
        user = database.update((current_user.age, current_user.email_id,current_user.image_file,current_user.username),update_query)
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
        # event = Event(title = form.title.data, description = form.description.data, author = current_user)
        # db.session.add(event)
        # db.session.commit()
        database = dbconnection()
        insert_query = "insert into events(event_name, created_by, event_category, start_date, end_date, cost_per_person, link_to_connect, max_capacity, location, criteria, event_description , event_status, min_age, max_age , event_city , event_state , covid_test) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        database.insert((form.title.data, form.description.data, form.email.data, form.age.data),insert_query)
        flash(f'Your event has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_event.html', title='New Event', form = form, legend = 'New Event', current_user = current_user)

@app.route('/event/<int:event_id>')
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event.html', title=event.title,event=event, current_user = current_user)

@app.route('/event/<int:event_id>/update', methods = ['GET', 'POST'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        db.session.commit()
        flash('Your event has been updated!', 'success')
        return redirect(url_for('event',event_id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
    return render_template('create_event.html', title='Update Event',event=event, form = form, legend = 'Update Event')

@app.route('/event/<int:event_id>/delete', methods = ['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_events(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    events = Event.query.filter_by(author=user)\
        .order_by(Event.date_added.desc())\
        .paginate(per_page=5, page = page)
    return render_template('user_events.html', events=events, user=user)