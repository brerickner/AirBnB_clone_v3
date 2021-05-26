#!/usr/bin/python3
"""Create a new view for Amenity objects that handles all
default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity
import json


@app_views.route('/amenities')
def amenities():
    """Retrieves all amenities"""
    obj_list = []
    for amenity in storage.all('Amenity').values():
        obj_list.append(amenity.to_dict())
    return jsonify(obj_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities_id(amenity_id):
    """Gets an amenity by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenities_id(amenity_id):
    """Deletes an amenity by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def post_amenities_id():
    amenity = request.get_json()
    if not amenity:
        abort(400, "Not a JSON")
    if 'name' not in amenity:
        abort(400, "Missing name")
    amen_var = Amenity(**amenity)
    storage.new(amen_var)
    storage.save()
    return(amen_var.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity_id(amenity_id):
    """Updates an amenity by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    amen = request.get_json()
    if amen is None:
        abort(400, "Not a JSON")
    for key, value in amen.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
