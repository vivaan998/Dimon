import logging
from flask import session, render_template, jsonify
from data.db import select_query, query_execute
import os, cv2
from app import module_directory
from datetime import datetime


def get_logs():
    logging.info('Running fetch logs...')
    if 'user_name' in session:
        logs = select_query("SELECT * FROM logs ORDER BY created_timestamp")
        return render_template('logs.html', username=session['user_name'], logs=logs, role=session['role'])
    else:
        return render_template('index.html', unauthorized=True)


def process_top_frame(view, metric):
    try:
        # put your algorithm here and for messages to show on front-end refer the code in accounts.py file
        # where if condition also return success or error.....
        view1 = None
        length = None
        width = None
        blacks_counts = None
        dimensions = str(length) + " x " + str(width)
        # stores original image
        main_name = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
        file_name = 'top-' + main_name
        path = os.path.join(module_directory, 'Images/Original/' + main_name)
        cv2.imwrite(path, view)

        # stores processed image
        path1 = os.path.join(module_directory, 'Images/top_view/' + file_name)
        cv2.imwrite(path1, view1)

        # insert into DB
        try:
            log = query_execute("INSERT INTO logs (log_class, image, dimensions) values (?,?,?)",
                                (
                                    blacks_counts,
                                    path1,
                                    dimensions
                                )
                                )
            if log:
                return jsonify({
                    'message': 'Success'
                }), 200

        except Exception as e:
            logging.error('Failed to save top frame. Message: %s', e)
            return jsonify({
                'message': 'Failed to save top frame.'
            }), 500
    except Exception as e:
        logging.error('Failed to process top frame. Message: %s', e)
        return jsonify({
            'message': 'Failed to process top frame. Contact support for assistance.'
        }), 500


def process_side_frame(view, metric):
    try:
        # put your algorithm here and for messages to show on front-end refer the code in accounts.py file
        # where if condition also return success or error.....
        view1 = None
        height = None
        height1 = None
        blacks_counts = None
        dimensions = str(height) + " x " + str(height1)
        # stores original image
        main_name = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
        file_name = 'side-' + main_name

        path = os.path.join(module_directory, 'Images/Original/' + main_name)
        cv2.imwrite(path, view)

        # stores processed image
        path1 = os.path.join(module_directory, 'Images/side_view/' + file_name)
        cv2.imwrite(path1, view1)

        # insert into DB
        try:
            log = query_execute("INSERT INTO logs (log_class, image, dimensions) values (?,?,?)",
                                (
                                    blacks_counts,
                                    path1,
                                    dimensions
                                )
                                )
            if log:
                return jsonify({
                    'message': 'Success'
                }), 200

        except Exception as e:
            logging.error('Failed to save top frame. Message: %s', e)
            return jsonify({
                'message': 'Failed to save top frame.'
            }), 500
    except Exception as e:
        logging.error('Failed to process top frame. Message: %s', e)
        return jsonify({
            'message': 'Failed to process top frame. Contact support for assistance.'
        }), 500
