from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
#import logging
import os
import numpy as np
import cv2
from artsfer import artsfer
import os
from PIL import Image

'''log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)'''

UPLOAD_FOLDER = '/upload'

app = Flask(__name__)
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@socketio.on('upload')
def handle_message(data):
    epochs = data['epochs']
    contentImageStr = data['contentImage']
    styleImageStr = data['styleImage']

    contentImage = cv2.imdecode(np.fromstring(
        contentImageStr, np.uint8), cv2.IMREAD_UNCHANGED)

    contentImage = cv2.cvtColor(contentImage, cv2.COLOR_BGR2RGB)

    styleImage = cv2.imdecode(np.fromstring(
        styleImageStr, np.uint8), cv2.IMREAD_UNCHANGED)

    styleImage = cv2.cvtColor(styleImage, cv2.COLOR_BGR2RGB)

    artsfer(contentImage, styleImage, epochs, emit,
            os.path.join(app.root_path, 'static/results'))


if __name__ == '__main__':
    socketio.run(app)
