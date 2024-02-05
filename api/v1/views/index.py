#!/usr/bin/python3
''' this is '''

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status_json():
    return jsonify({"status": "OK"}), 200


classes = {"Amenities": Amenity, "Cities": City, "Places": Place,
           "Reviews": Review, "States": State, "Users": User}


@app_views.route('/stats', strict_slashes=False)
def stat():
    new_dict = {}
    for k, v in classes.items():
        new_dict[k.lower()] = storage.count(v)
    return jsonify(new_dict)
