import os
import logging
import cv2

from datetime import timedelta, datetime
from flask import Flask, render_template, request, session, redirect, url_for, Response

from config.accounts import login_service, add_user, get_users, update_user, delete_user
from config.log_data import get_logs
from config.streaming import gen_frames, genSecondary_frames, firstCapture, secondCapture, main_execution
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


@application.route('/top_view_capture', methods=['POST'])
def top_view_capture():
    return main_execution(firstCapture(), request.form['metricValue'], 'top_view')


@application.route('/side_view_capture', methods=['POST'])
def side_view_capture():
    return main_execution(secondCapture(), request.form['metricValue'], 'side_view')


@application.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    if 'user_name' in session:
        return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return render_template('index.html', unauthorized=True)


@application.route('/secondary_feed')
def secondary_feed():
    camera2 = cv2.VideoCapture(1)
    if 'user_name' in session:
        return Response(genSecondary_frames(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return render_template('index.html', unauthorized=True)


@application.route('/stream')
def stream():
    if 'user_name' in session:
        logging.info('Running stream...')
        return render_template('streaming.html', username=session['user_name'], role=session['role'])
    else:
        return render_template('index.html', unauthorized=True)


@application.route('/users', methods=['GET', 'PUT', 'DELETE'])
def users():
    if 'user_name' and 'role' in session and session['role'] == 'admin':
        if request.method == 'GET':
            return get_users()
        elif request.method == 'PUT':
            return update_user(request.json)
        else:
            return delete_user(request.json)
    else:
        return render_template('index.html', unauthorized=True)


@application.route('/users_add', methods=['GET', 'POST'])
def users_add():
    if 'user_name' and 'role' in session and session['role'] == 'admin':
        if request.method == 'POST':
            return add_user(request.json)
        if 'id' in request.args:
            user = select_query("SELECT * FROM users where id=" + request.args['id'])
            return render_template('add_user.html', username=session['user_name'], role=session['role'], user=user[0])
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
