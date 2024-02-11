#!/usr/bin/python3
'''This is all about places'''

from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from markupsafe import escape


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"])
@app_views.route('/places/<place_id>', methods=["GET", "PUT", "DELETE"])
def place_handler(place_id='', city_id='', user_id=''):
    get_place = storage.all(Place)
    get_city = storage.all(City)
    get_user = storage.all(User)
    id_place = 'Place.' + place_id if place_id else ''
    id_city = 'City.' + city_id if city_id else ''
    id_user = 'User.' + user_id if user_id else ''
    if request.method == 'GET':
        if city_id:
            if not get_city.get(id_city):
                abort(404)
            return jsonify([v.to_dict() for v in get_place.values() if id_city == v.city_id])
        if place_id:
            if not get_place.get(id_place):
                abort(404)
            ans = get_place.get(id_place)
            return jsonify(ans.to_dict())
    if request.method == "DELETE":
        if not get_place.get(id_place):
            abort(404)
        ans = get_place.get(id_place)
        storage.delete(ans)
        storage.save()
        return jsonify({}), 200
    if request.method == "POST":
        if request.is_json:
            json_get = request.get_json()
        else:
            abort(400, 'Not a JSON')
        if not json_get.get('user_id'):
            abort(400, 'Missing user_id')
        elif not json_get.get('name'):
            abort(400, 'Missing name')
        else:
            new = Place(**json_get)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201
    if request.method == "PUT":
        if not get_place.get(id_place):
            abort(404)
        if request.is_json:
            json_get = request.get_json()
        else:
            abort(400, 'Not a JSON')
        upd_place = get_place.get(id_place)
        for k, v in json_get.items():
            if not k in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(upd_place, k, v)
        storage.save()
        return jsonify(upd_place.to_dict()), 200
