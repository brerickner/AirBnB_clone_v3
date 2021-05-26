#!/usr/bin/python3
"""Create a new view for City objects that handles all
default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_by_state(state_id):
    """Gets all cities belonging to a state_id"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    city_list = []
    for city in storage.all('City').values():
        if(city.state_id == state_id):
            city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def cities_id(city_id):
    """Retrieves a specific city by id"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city_id(city_id):
    """Deletes a city by id"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def post_city(state_id):
    """Creates a new city in the state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = request.get_json()
    if not city:
        abort(400, "Not a JSON")
    if 'name' not in city:
        abort(400, "Missing name")
    city['state_id'] = state_id
    city_var = City(**city)
    storage.new(city_var)
    storage.save()
    return(city_var.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city_id(city_id):
    """Updates a city by id"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    city = request.get_json()
    if city is None:
        abort(400, "Not a JSON")
    for key, value in city.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
