import os
import logging
from datetime import timedelta
from flask import Flask, render_template, request, session, redirect, url_for, Response

from config.accounts import login_service, add_user, get_users, update_user, delete_user
from config.log_data import get_logs
from config.streaming import gen_frames, genSecondary_frames, firstCapture, secondCapture
from data.db import select_query
import cv2



module_directory = os.path.dirname(os.path.realpath(__file__))

application = Flask(__name__)
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



camera = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)

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




@application.route('/first_capture', methods=['POST'])
def first_capture():
    print('>>>> FRAME CAPTURE FROM FIRST CAMERA <<<<')
    data = request.form['metricValue']
    capture = firstCapture()        
    print('Metric value - ', data)
    print('First camera frame - ', capture)
    cv2.imwrite('FirstCamCapture.jpg', capture)
    return str(capture)

@application.route('/second_capture', methods=['POST'])
def second_capture():
    print('>>>> FRAME CAPTURE FROM SECOND CAMERA <<<<')
    data = request.form['metricValue']
    capture = secondCapture()        
    print('Metric value - ', data)
    print('Second camera frame - ', capture)
    cv2.imwrite('SecondCamCapture.jpg', capture)
    return str(capture)



@application.route('/video_feed')
def video_feed():
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@application.route('/secondary_feed')
def secondary_feed():
    return Response(genSecondary_frames(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')



@application.route('/test')
def test():
    print('Running Test...')
    return render_template('test.html')




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
    application.run(host='127.0.0.1', port=5000)
