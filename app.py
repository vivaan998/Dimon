import os
import logging
from datetime import timedelta
from flask import Flask, render_template, request, session, redirect, url_for

from config.accounts import login_service

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
def mains():
    logging.info('Running dashboard...')
    if 'user_name' in session:
        return render_template('dashboard.html', username=session['user_name'])
    else:
        return render_template('index.html', unauthorized=True)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
