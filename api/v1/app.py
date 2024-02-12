#!/usr/bin/python3
''' This is something'''

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

Host = getenv('HBNB_API_HOST')
Port = getenv('HBNB_API_PORT')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    storage.close()


@app.errorhandler(404)
def checkError404(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=Host, port=int(Port), threaded=True)
