#!/usr/bin/python3
'''This is all about '''

from markupsafe import escape
from api.v1.views import app_views
from models.state import State
from models.base_model import BaseModel, Base
from models import storage
from flask import request, jsonify, abort


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def base_id(state_id=None):
    get_all = storage.all(State)
    if request.method == "GET":
        if state_id:
            try:
                k = 'State'+'.' + state_id
                return jsonify(get_all[k].to_dict())
            except KeyError:
                abort(404)
        else:
            l = [v.to_dict() for k, v in get_all.items()]
            return jsonify(l)
    if request.method == "DELETE":
        if state_id:
            try:
                k = 'State'+'.' + escape(state_id)
                storage.delete(get_all[k])
                storage.save()
                return jsonify({}), 200
            except KeyError:
                abort(404)
    if request.method == "POST":
        if request.is_json:
            json_get = request.get_json()
        else:
            abort(400, "Not a JSON")
        if json_get['name']:
            new_inst = State(**json_get)
            storage.new(new_inst)
            storage.save()
            return jsonify(new_inst.to_dict()), 201
        else:
            abort(400, 'Missing name')

    if request.method == "PUT":
        try:
            k = 'State.' + state_id
            new = get_all[k]
            if request.is_json:
                json_get = request.get_json()
            else:
                abort(400, "Not a JSON")
            for k, v in json_get.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(new, k, v)
            storage.save()
            return jsonify(new.to_dict()), 200
        except KeyError:
            abort(404)
