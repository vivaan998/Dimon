import cv2
import logging
from flask import jsonify
from config.log_data import process_frame


def firstCapture():
    return FIRST_CAMERA


def secondCapture():
    return SECOND_CAMERA


def gen_frames(camera):
    global FIRST_CAMERA
    while True:
        success, frame = camera.read()  # read the camera frame
        frame = cv2.flip(frame, 1)
        FIRST_CAMERA = frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def genSecondary_frames(camera2):
    global SECOND_CAMERA
    while True:
        success, frame = camera2.read()  # read the camera frame
        frame = cv2.flip(frame, 1)
        SECOND_CAMERA = frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def main_execution(view, metric, view_type):
    logging.info('Running main_execution...')
    if view_type == 'top_view':
        global TOP_VIEW
        global TOP_METRIC
        TOP_VIEW = view
        TOP_METRIC = metric
        return jsonify({
            'message': 'Successfully captured'
          }), 200
    else:
        if TOP_VIEW and TOP_METRIC:
            return process_frame(TOP_VIEW, TOP_METRIC, view, metric)
