import os
import logging
from datetime import timedelta
from flask import Flask, render_template, request, session, redirect, url_for

from config.accounts import login_service, add_user, get_users, update_user, delete_user
from config.log_data import get_logs
from data.db import select_query

module_directory = os.path.dirname(os.path.realpath(__file__))

application = Flask(__name__)
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@application.before_request
def make_session_permanent():
    session.permanent = True
    application.permanent_session_lifetime = timedelta(minutes=5)


@application.route('/')
def index():
    return render_template('index.html', unauthorized=False)


# ############### Account ################################
@application.route('/login', methods=['POST'])
def login():
    return login_service(request.json['username'], request.json['password'])


@application.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('email', None)
    session.pop('role', None)
    return redirect(url_for('index'))


@application.route('/dashboard')
def dashboard():
    logging.info('Running dashboard...')
    if 'user_name' in session:
        return render_template('dashboard.html', username=session['user_name'], role=session['role'])
    else:
        return render_template('index.html', unauthorized=True)


@application.route('/users', methods=['GET', 'PUT', 'DELETE'])
def users():
    print(request.method)
    if 'user_name' and 'role' in session and session['role'] == 'admin':
        if request.method == 'GET':
            return get_users()
        elif request.method == 'PUT':
            return update_user(request.json)
        else:
            return delete_user(request.json)
    else:
        return render_template('index.html', unauthorized=True)


@application.route('/users_add', methods=['GET', 'POST', 'PUT'])
def users_add():
    if 'user_name' and 'role' in session and session['role'] == 'admin':
        if request.method == 'POST':
            return add_user(request.json)
        if request.method == 'PUT':
            user = select_query("SELECT * FROM users where id=" + request.json['id'])
            return render_template('add_user.html', username=session['user_name'], role=session['role'], user=user)
        else:
            return render_template('add_user.html', username=session['user_name'], role=session['role'])
    else:
        return render_template('index.html', unauthorized=True)


@application.route('/logs', methods=['GET'])
def logs():
    if 'user_name' and 'role' in session and session['role'] == 'admin':
        return get_logs()
    else:
        return render_template('index.html', unauthorized=True)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
