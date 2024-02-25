#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import json
import ufr

# import camera driver
from camera_ufr import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/data')
def robot_data_feed():
    link = ufr.Link("@new mqtt:topic @host 185.209.160.8 @topic robo/pose @coder msgpack:obj")
    link.start_subscriber()
    valores = link.get("^ii")
    data = {"pose": valores}
    return json.dumps(data)

@app.route('/motor')
def robot_motor_set():
    link = ufr.Link("@new mqtt:topic @host 185.209.160.8 @topic robo/motor @coder msgpack:obj")
    link.start_publisher()
    link.putln("iiii", 10,20,30,40)
    # link.close()
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
