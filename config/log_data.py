import logging
from flask import session, render_template
from data.db import select_query


def get_logs():
    logging.info('Running fetch logs...')
    if 'user_name' in session:
        logs = select_query("SELECT * FROM logs ORDER BY created_timestamp")
        return render_template('users.html', username=session['user_name'], logs=logs)
    else:
        return render_template('index.html', unauthorized=True)
