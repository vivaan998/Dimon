import cv2
import logging
from flask import jsonify
from config.log_data import process_frame
import pickle


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
        # Storing top view and metric to a temporary storage
        with open('tempTOP_CAMERA_STORAGE.pkl', 'wb') as f: 
            pickle.dump([view, metric], f)
        return jsonify({
            'message': 'Success'
          }), 200

    else:
        # Getting back the top view and metric
        with open('tempTOP_CAMERA_STORAGE.pkl', 'rb') as f: 
            top_view, top_metric = pickle.load(f)

        # Setting None again to temp storage
        with open('tempTOP_CAMERA_STORAGE.pkl', 'wb') as f: 
            pickle.dump([None, None], f)

        if top_metric:
            return process_frame(top_view, top_metric, view, metric)
        else:
            return jsonify({
                'message': 'Please capture top view'
            }), 200
