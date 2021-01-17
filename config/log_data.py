import logging
from flask import session, render_template, jsonify
from data.db import select_query, query_execute
import os, cv2
from configuration import module_directory
from datetime import datetime


def get_logs():
    logging.info('Running fetch logs...')
    if 'user_name' in session:
        logs = select_query("SELECT * FROM logs ORDER BY created_timestamp")
        return render_template('logs.html', username=session['user_name'], logs=logs, role=session['role'])
    else:
        return render_template('index.html', unauthorized=True)


def process_frame(top_view, top_metric, side_view, side_metric):
    try:

        processed_top_view, length, width, blacks_counts = xyz(top_view, top_metric)

        processed_side_view, height, height1 = abc(side_view, side_metric)

        dimensions = "[" + str(length) + " x " + str(width) + "]  [" + str(height) + " x " + str(height1) + "]"
        # stores top original image
        top_name = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
        original_top_path = os.path.join(module_directory, 'Images/Original/' + top_name)
        cv2.imwrite(original_top_path, top_view)

        # stores top processed image
        top_file_name = 'top-' + top_name
        top_path = os.path.join(module_directory, 'Images/top_view/' + top_file_name)
        cv2.imwrite(top_path, processed_top_view)

        # stores side original image
        side_name = datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg'
        original_side_path = os.path.join(module_directory, 'Images/Original/' + side_name)
        cv2.imwrite(original_side_path, side_view)

        # stores side processed image
        side_file_name = 'side-' + side_name
        side_path = os.path.join(module_directory, 'Images/side_view/' + side_file_name)
        cv2.imwrite(side_path, processed_side_view)

        images = top_path + ", " + side_path
        # insert into DB
        try:
            log = query_execute("INSERT INTO logs (log_class, image, dimensions) values (?,?,?)",
                                (
                                    blacks_counts,
                                    images,
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


def xyz(view, metric):
    pass


def abc(view, metric):
    pass
