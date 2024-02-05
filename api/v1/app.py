#!/usr/bin/python3
''' This is something'''

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

Host = getenv('HBNB_API_HOST')
Port = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def checkError(self):
    storage.close()

if __name__ == '__main__':
    app.run(host=Host, port=int(Port), threaded=True)
