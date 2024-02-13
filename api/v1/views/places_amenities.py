#!/usr/bin/python3
''' working on places amenity '''

from flask import abort, request, jsonify
from markupsafe import escape
from models.amenity import Amenity
from models.place import Place
from models import storage
from api.v1.views import app_views
from os import getenv


@app_views.route('/places/<place_id>/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/places/<place_id>/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE', 'POST'])
def place_amenities_handler(place_id='', amenity_id=''):
    all_pls = storage.all(Place)
    all_amen = storage.all(Amenity)
    id_pls = 'Place.' + escape(place_id) if place_id else ''
    id_amen = 'Amenity.' + escape(amenity_id) if amenity_id else ''
    if request.method == 'GET':
        if place_id:
            if not all_pls.get(id_pls):
                abort(404)
            l = []
            r = all_pls.get(id_pls)
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                for x in r.amenities:
                    l.append(x.to_dict())
                return jsonify(l)
            else:
                r = r.to_dict()
                for k in r.get('amenity_ids'):
                    kss = 'Amenity.' + k
                    re = all_amen.get(kss)
                    l.append(re.to_dict())
                return jsonify(l)
    if request.method == 'DELETE':
        if not all_pls.get(id_pls):
            abort(404)
        if not all_amen.get(id_amen):
            abort(404)
        amen = all_amen.get(id_amen)
        pls = all_pls.get(id_pls)
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if not amen in pls.amenities:
                abort(404)
            pls.amenities = [a for a in pls.amenities if a != amen]
            storage.save()
            return jsonify({}), 200
        else:
            pls = pls.to_dict()
            dict_amen = pls.get('amenity_ids')
            if not amen.id in dict_amen:
                abort(404)
            dict_amen.remove(amen.id)
            storage.save()
            return jsonify({}), 200
