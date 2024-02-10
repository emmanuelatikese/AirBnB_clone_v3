#!/usr/bin/python3
'''This is all about users'''

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from markupsafe import escape


@app_views.route('/users', methods=["GET", "POST"])
@app_views.route('/users/<user_id>', methods=["GET", "PUT", "DELETE"])
def user_handler(user_id=''):
    get_user = storage.all(User)
    id_user = 'User.' + user_id if user_id else ''
    if request.method == 'GET':
        if not user_id:
            return jsonify([v.to_dict() for v in get_user.values()])
        else:
            if get_user.get(id_user):
                ans = get_user.get(id_user)
                return jsonify(ans.to_dict())
            else:
                abort(404)
    if request.method == "DELETE":
        if get_user.get(id_user):
            ans = get_user.get(id_user)
            storage.delete(ans)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    if request.method == "POST":
        if request.is_json:
            json_get = request.get_json()
        else:
            abort(400, 'Not a JSON')
        if not json_get.get('email'):
            abort(400, 'Missing email')
        elif not json_get.get('password'):
            abort(400, 'Missing password')
        else:
            new = User(**json_get)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201
    if request.method == "PUT":
        if not get_user.get(id_user):
            abort(404)
        if request.is_json:
            json_get = request.get_json()
        else:
            abort(400, 'Not a JSON')
        upd_user = get_user.get(id_user)
        for k, v in json_get.items():
            if not k in ['id', 'email', 'created_at', 'updated_at']:
                setattr(upd_user, k, v)
        storage.save()
        return jsonify(upd_user.to_dict()), 200
