import os
import csv
import logging
from pyapp import bp
from flask import Flask
from pyadmin import admin
from flask_cors import CORS
from pyadmin import login_manager

app = Flask(__name__)
app.config["SESSION_COOKIE_HTTPONLY"] = False
app.config["SECRET_KEY"] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'
CORS(app)

app.register_blueprint(bp)
admin.init_app(app)
login_manager.init_app(app)

path = app.instance_path
if not os.path.exists(path):
    os.makedirs(path)

"""
filePath = os.path.join(app.instance_path, 'event_log.csv')
with open(filePath, 'w', newline='') as eventLog:
    writer = csv.writer(eventLog)
    writer.writerow(["Date", "User", "Category", "Action", "Param1", "Param2"])
"""

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    app.run(debug=True,port=8000)
