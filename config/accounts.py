import logging
from flask import session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from data.db import select_one_query

def login_service(username, password):
    logging.info('Running login...')
    try:
        user = select_one_query(f"SELECT * FROM users WHERE email="+ username)
        if user and 'email' in user and 'password' in user:
            if user['email'] == username and check_password_hash(user['password'], password):
                session['user_name'] = user['display_name'] if 'display_name' in user else None
                session['email'] = user['email']
                session['role'] = user['role']
                return jsonify({
                        'message': 'Successfully logged in'
                    })
            else:
                logging.info("Invalid User details")
                return jsonify({
                        'message': 'Invalid User details'
                    }), 400
        else:
            logging.info("User details not found")
            return jsonify({
                        'message': 'User details not found'
                    }), 400
    except Exception as e:
        logging.error('Failed to login. Message: %s', e)
        return jsonify({
            'message': 'Something went wrong. Contact support for assistance.'
        }), 500