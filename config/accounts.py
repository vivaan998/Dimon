import logging
from flask import session, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from data.db import select_one_query, query_execute, select_query


def login_service(username, password):
    logging.info('Running login...')
    try:
        user = select_one_query(f"SELECT * FROM users WHERE email='" + username + "'")
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


def get_users():
    logging.info('Running fetch users...')
    if 'user_name' in session:
        users = select_query("SELECT * FROM users where role='user'")
        return render_template('users.html', username=session['user_name'], users=users, role=session['role'])
    else:
        return render_template('index.html', unauthorized=True)


def add_user(data):
    logging.info('Running add users...')
    try:
        email = select_query("SELECT * FROM users where email='" + data['email'] + "'")
        if email:
            return jsonify({
                'message': 'Email Already Exists'
            }), 400
        else:
            user = query_execute("INSERT INTO users (email, password, role, display_name) values (?,?,?,?)",
                                 (
                                     data['email'],
                                     generate_password_hash(data['password']),
                                     data['role'],
                                     data['display_name'],
                                 )
                                 )
            if user:
                return jsonify({
                    'message': 'User created successfully'
                }), 200
    except Exception as e:
        logging.error('Failed to add user. Message: %s', e)
        return jsonify({
            'message': 'Something went wrong. Contact support for assistance.'
        }), 500


def update_user(data):
    logging.info('Running update users...')
    try:
        if (data['password'] != ''):
            query = "UPDATE users SET email=?, password=?, display_name=? WHERE id=" + data['id']
            value = (data['email'], generate_password_hash(data['password']), data['display_name'])
            
        else:
            query = "UPDATE users SET email=?, display_name=? WHERE id=" + data['id']
            value = (data['email'], data['display_name'])
            user = query_execute(query, data=value)
           
        user = query_execute(query, data=value)
        return jsonify({
            'message': 'User updated successfully'
        }), 200  
    except Exception as e:
        logging.error('Failed to update. Message: %s', e)
        return jsonify({
            'message': 'Something went wrong. Contact support for assistance.'
        }), 500


def delete_user(data):
    logging.info('Running update users...')
    try:
        if 'id' not in data:
            return jsonify({
                'message': 'Id not present'
            }), 400
        user = query_execute("DELETE FROM users WHERE id=" + data['id'])
        if user:
            return jsonify({
                'message': 'User deleted successfully'
            }), 200
    except Exception as e:
        logging.error('Failed to delete user. Message: %s', e)
        return jsonify({
            'message': 'Something went wrong. Contact support for assistance.'
        }), 500
