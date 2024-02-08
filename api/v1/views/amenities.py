#!/usr/bin/python3
'''This all about amenities '''
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/api/v1/amenities', methods=['GET', 'POST', ], strict_slashes=False)
@app_views.route('/api/v1/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_handler(amenity_id=''):
    id_amen = 'Amenity.' + amenity_id if amenity_id else ''
    all_amen = storage.all(Amenity)
    if request.method == 'GET':
        if amenity_id and all_amen.get(id_amen):
            return jsonify(all_amen[id_amen].to_dict())
        else:
            abort(404)
        return jsonify([v.to_dict() for v in all_amen.values()])
    if request.method == 'DELETE':
        if all_amen.get(id_amen):
            return jsonify({}), 200
        else:
            abort(404)
    if request.method == 'POST':
        if request.is_json:
            new_inst = request.get_json()
            if new_inst.get('name'):
                new_amen = Amenity(new_inst)
                storage.new(new_amen)
                storage.save()
                return jsonify(new_amen.to_dict()), 201
            else:
                abort(404, 'Missing name')
        else:
            abort(404, 'Not a JSON')
    if request.method == 'PUT':
        if amenity_id and all_amen[id_amen]:
            if request.is_json:
                new_dict = request.get_json()
                new_json = all_amen[id_amen]
                for k, v in new_dict.items():
                    if k != 'id' and k != 'created_at' and k != 'updated_at':
                        setattr(Amenity, k, v)
                storage.save()
                return jsonify(new_json.to_dict()), 200
            else:
                abort(404, 'Not a JSON')
        else:
            abort(404)
