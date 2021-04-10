# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging
import mysql.connector

from flask import Flask,jsonify,request,render_template


app = Flask(__name__)

@app.route('/')
@app.route('/home') 
def home():
    #page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page = page)
    return render_template('home.html')

@app.route('/login')
def login():
    user_name=request.args.get('name')
    password=request.args.get('password')
    confirm_password=request.args.get('confirm_password')
    login_status=dict()
    if(password!=confirm_password):
        login_status['status']='password and conform password are not same'
    else:
        login_status['status']='Login Successful for '+user_name
        mydb = mysql.connector.connect(
                    host="34.106.21.213",
                    user="teja",
                    password="teja1234",
                    database="test"
                )

        mycursor = mydb.cursor()

        sql = "INSERT INTO testing (username, password) VALUES (%s, %s)"
        val = (user_name, password)
        mycursor.execute(sql, val)
        mydb.commit()
    return jsonify(login_status)

@app.route('/register')
def register():
    user_name=request.args.get('name')
    password=request.args.get('password')
    confirm_password=request.args.get('confirm_password')
    mobile_number=request.args.get('mobile_number')
    age=request.args.get('age')
    email=request.args.get('emial')
    register_status=dict()
    register_status['status']='Registration Successful'
    return jsonify(register_status)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]