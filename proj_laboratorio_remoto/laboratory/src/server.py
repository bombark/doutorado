# Copyright (C) 2024  Felipe Bombardelli <felipebombardelli@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.



import ufr
import cv2
from flask import Flask, render_template, Response

"""
image = ufr.Link("@new mqtt:topic @host 185.209.160.8 @topic teste @coder msgpack:obj")
image.start_subscriber()

for i in range(50):
    print("opa")
    image.recv()
    print(" opa1")
    data = image.read()
    data.tofile("teste.jpg")
    print(" opa2")
    img = cv2.imread("teste.jpg")
    cv2.imshow("imagem", img)
    cv2.waitKey(10)
"""

def gen():
    # while True:
    fd = open("teste.jpg", "rb")
    frame = fd.read()
    fd.close()
    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response( gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)