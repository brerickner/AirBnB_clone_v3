#!/usr/bin/python3
"""Create a new view for Amenity objects that handles all
default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
import json


@app_views.route('/users', methods=['GET'])
def users():
    """Retrieves all users"""
    obj_list = []
    for user in storage.all('User').values():
        obj_list.append(user.to_dict())
    return jsonify(obj_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def users_id(user_id):
    """Retrieves user by id"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user_id(user_id):
    """Deletes a user by id"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def post_user_id():
    """Creates a user"""
    user = request.get_json()
    if not user:
        abort(400, "Not a JSON")
    if 'email' not in user:
        abort(400, "Missing email")
    if 'password' not in user:
        abort(400, "Missing password")
    user_var = User(**user)
    storage.new(user_var)
    storage.save()
    return(user_var.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user_id(user_id):
    """Updates user by id"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    user = request.get_json()
    if user is None:
        abort(400, "Not a JSON")
    for key, value in user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
