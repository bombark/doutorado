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

# =============================================================================
#  Header
# =============================================================================

from datetime import datetime
from dataclasses import dataclass
from flask import Flask, render_template, request
import threading
import ufr
import json
import random

g_unit_x86 = ufr.Client("@new zmq:socket @port 4000 @coder msgpack:obj")

# =============================================================================
#  Main
# =============================================================================

app = Flask(__name__)

@app.route('/')
def index():
    # renderiza
    return render_template('index.html')

@app.route('/dados.json')
def index_json():
    g_unit_x86.putln("get_data")
    data = g_unit_x86.get("^ss")
    if data[0] == "OK":
        return data[1]
    return "ERROR"

@app.route('/exec')
def exec():
    line = request.args.get('line')
    g_unit_x86.putln("exec", line)
    is_ok = g_unit_x86.get("^s")
    if is_ok == "ERROR":
        error_msg = g_unit_x86.get("s")
        return json.dumps({'state': is_ok, 'msg': error_msg})

    return json.dumps({'state': 'OK'})

if __name__ == '__main__':
    app.run(port=3000, debug=True)