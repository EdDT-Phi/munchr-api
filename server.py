from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import utils
import logging
import users
import restaurants
import os
from err import InvalidUsage

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)


@app.route('/restaurants/', methods=['GET', 'POST'])
def get_restaurants():
    if request.method == 'GET':
        # return render_template('restaurants.html', data=restaurants.get_filters(30.3, -97.7))
        return render_template('restaurants.html')

    lat = utils.get_float(request, 'lat', required=True)
    lng = utils.get_float(request, 'long', required=True)
    rad = utils.get_num(request, 'radius', 1, 20, required=True)
    cuisines = utils.get_list(request, 'cuisines')
    price = utils.get_num(request, 'price', required=True)
    user_id = utils.get_num(request, 'user_id', required=True)

    return restaurants.get_restaurants(lat, lng, rad, price, cuisines)


@app.route('/restaurants/filters', methods=['GET', 'POST'])
def get_filters():
    if request.method == 'GET':
        return render_template('filters.html')

    lat = utils.get_field(request, 'lat', required=True)
    lng = utils.get_field(request, 'long', required=True)

    return restaurants.get_filters(lat, lng)


@app.route('/restaurants/details/<string:place_id>')
def get_details(place_id):
    return restaurants.get_details(place_id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = utils.get_field(request, 'email', required=True)
    password = utils.get_field(request, 'password', required=True)
    return users.login(email, password, bcrypt)


@app.route('/friends/', methods=['GET', 'POST'])
@app.route('/friends/<int:user_id>')
def friends(user_id=None):
    if user_id is None and request.method == 'GET':
        return render_template('new_friend.html')

    if request.method == 'POST':
        user_id1 = utils.get_num(request, 'user_id1', required=True)
        user_id2 = utils.get_num(request, 'user_id2', required=True)

        return users.new_friend(user_id1, user_id2)

    return users.get_friends(user_id)


@app.route('/users/search/', methods=['GET', 'POST'])
def users_search():
    if request.method == 'GET':
        return render_template('search.html')

    query = utils.get_field(request, 'query', required=True)
    user_id = utils.get_num(request, 'user_id', required=True)
    return users.search_users(query, user_id)


@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>')
def users_route(user_id=None):
    if request.method == 'POST':
        first_name = utils.get_field(request, 'first_name', required=True)
        last_name = utils.get_field(request, 'last_name', required=True)
        email = utils.get_field(request, 'email', required=True)
        password = utils.get_field(request, 'password')
        fb_id = utils.get_field(request, 'fb_id')
        photo = utils.get_field(request, 'photo')

        return users.new_user(first_name, last_name, email, password, fb_id, photo)

    if user_id is None:
        return users.get_all_users()

    return users.get_user(user_id)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    port = int(os.environ.get('MUNCHR_PORT') or 5000)
    app.run(debug=(not os.environ.get('MUNCHR_PROD') == 'FALSE'), port=port, host='0.0.0.0')
