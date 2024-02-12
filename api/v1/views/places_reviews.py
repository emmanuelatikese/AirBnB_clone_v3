#!/usr/bin/python3
'''This is about another thing'''

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from markupsafe import escape

app_views.route('/places/<place_id>/reviews', methods=['GET', 'POSt'])
app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])


def handler_review(place_id='', review_id=''):
    all_rev = storage.all(Review)
    all_place = storage.all(Place)
    id_rev = 'Review.' + escape(review_id) if review_id else ''
    id_pl = 'Place.' + escape(place_id) if place_id else ''
    if request.method == 'GET':
        if place_id:
            if not all_place.get(id_pl):
                abort(404)
            empt = []
            for v in all_rev.values():
                if v.place_id == place_id:
                    empt.append(v.to_dict())
            return jsonify(empt)
        if review_id:
            if not all_rev.get(id_rev):
                abort(404)
            ans = all_rev.get(id_rev)
            return jsonify(ans.to_dict())
    if request.metod == 'DELETE':
        if not all_rev.get(id_rev):
            abort(404)
        ans = all_rev.get(id_rev)
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
        elif not json_get.get('text'):
            abort(400, 'Missing text')
        else:
            new = Review(**json_get)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201
    if request.method == "PUT":
        if not all_rev.get(id_rev):
            abort(404)
        if request.is_json:
            json_get = request.get_json()
        else:
            abort(400, 'Not a JSON')
        upd_place = all_rev.get(id_rev)
        for k, v in json_get.items():
            if not k in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(upd_place, k, v)
        storage.save()
        return jsonify(upd_place.to_dict()), 200
