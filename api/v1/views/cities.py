#!/usr/bin/python3
''' this is about citeis'''

from api.v1.views import app_views
from models.city import City
from flask import abort, request, jsonify
from models import storage
from markupsafe import escape
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['DELETE', 'PUT', 'GET'], strict_slashes=False)
def cityhandler(state_id='', city_id=''):
    all_cities = storage.all(City)
    k = 'City.' + escape(city_id)
    if request.method == 'GET':
        if state_id:
            try:
                for v in all_cities.values():
                    return jsonify([v.to_dict() for v in all_cities.values() if v.state_id == state_id])
            except KeyError:
                abort(404)
        if city_id:
            try:
                ans = all_cities[k]
                return jsonify(ans.to_dict())
            except KeyError:
                abort(404)
    if request.method == 'DELETE':
        if all_cities[k]:
            storage.delete(all_cities[k])
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    if request.method == 'POST':
        states_list = storage.all(State)
        state_k = 'State.' + state_id
        if state_k not in states_list and not states_list[state_k]:
            abort(404)
        if request.is_json:
            json_get = request.get_json()
            if json_get['name']:
                json_get['state_id'] = state_id
                new_inst = City(**json_get)
                storage.new(new_inst)
                storage.save()
                return jsonify(new_inst.to_dict()), 201
            else:
                abort(400, 'Missing name')
        else:
            abort(400, "Not a JSON")

    if request.method == "PUT":
        if k not in all_cities:
            abort(404)
        try:
            if request.is_json:
                json_get = request.get_json()
            else:
                abort(400, "Not a JSON")
            new_inst = all_cities[k]
            for k, v in json_get.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(City, k, v)
            storage.save()
            return jsonify(new_inst.to_dict()), 200
        except KeyError:
            abort(404)
