#!/usr/bin/python3
"""Create a new view for Review object that
handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
import json


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def review_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    review_list = []
    for review in storage.all('Review').values():
        if(review.place_id == place_id):
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def reviews_id(review_id):
    """Retrieves a Review object"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_review_id(review_id):
    """Deletes a review by id"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews/', methods=['POST'])
def post_review(place_id):
    """Creates a new review in the place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review = request.get_json()
    if not review:
        abort(400, "Not a JSON")
    if 'user_id' not in review:
        abort(400, "Missing user_id")
    user = storage.get(User, review.get('user_id'))
    if user is None:
        abort(404)
    if 'text' not in review:
        abort(400, "Missing text")
    review['place_id'] = place_id
    review_var = Review(**review)
    storage.new(review_var)
    storage.save()
    return(review_var.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'])
def put_review_id(review_id):
    """Updates a Review object"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    review = request.get_json()
    if review is None:
        abort(400, "Not a JSON")
    for key, value in review.items():
        if key not in [
            'id',
            'user_id',
            'place_id',
            'created_at',
                'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
