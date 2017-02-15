from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL
import utils
import logging
from users import Users
import restaurants
import os
from err import InvalidUsage

app = Flask(__name__)
CORS(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('MYSQL_DATABASE')
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_DATABASE_PORT'] = int(os.environ.get('MYSQL_PORT'))
mysql.init_app(app)

print('Attempting to connect to databse')
conn = None
try:
	conn = mysql.connect()
	print('Connected to database')
except:
	print("I am unable to connect to the database")

users = Users(conn, Bcrypt(app))


@app.route('/restaurants/', methods=['GET', 'POST'])
def get_restaurants():
	if request.method == 'GET':
		return render_template('restaurants.html', data=restaurants.filters_object())

	lat = utils.get_field(request, 'lat', required=True)
	lng = utils.get_field(request, 'long', required=True)
	rad = utils.get_num(request, 'radius', required=True)
	cuisines = utils.get_list(request, 'cuisines', required=True)
	categories = utils.get_list(request, 'cuisines', required=True)
	price = utils.get_num(request, 'price', required=True)
	user_id = utils.get_num(request, 'user_id', required=True)

	return restaurants.get_restaurants(lat, lng, rad, cuisines, categories, price)


@app.route('/restaurants/filters', methods=['GET', 'POST'])
def get_filters():
	if request.method == 'GET':
		return render_template('filters.html')

	# lat = utils.get_field(request, 'lat', required=True)
	# lng = utils.get_field(request, 'long', required=True)

	return restaurants.get_filters()


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

	email = utils.get_field(request, 'email', required=True)
	password = utils.get_field(request, 'password', required=True)
	return users.login(email, password)


@app.route('/friends/', methods=['GET', 'POST'])
@app.route('/friends/<int:user_id>')
def friends(user_id=None):
	if user_id is None and request.method == 'GET':
		return render_template('new_friend.html')

	if request.method == 'POST':
		user_id1 = utils.get_num(request, 'user_id1', required=True)
		user_id2 = utils.get_num(request, 'user_id2', required=True)

		return users.new_friend(user_id1, user_id2)

	return get_friends(request, user_id)


@app.route('/users/search/', methods=['GET', 'POST'])
def users_search():
	if request.method == 'GET':
		return render_template('search.html')
	return search_users(request)


@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>')
def users_route(user_id=None):
	if request.method == 'POST':
		first_name = utils.get_field(request, 'first_name', required=True)
		last_name = utils.get_field(request, 'last_name', required=True)
		email = utils.get_field(request, 'email', required=True)
		password = utils.get_field(request, 'password')
		fb_id = utils.get_field(request, 'fb_id')

		return new_user(first_name, last_name, email, password, fb_id)

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
	app.run(debug=(os.environ.get('MUNCHR_PROD') == 'TRUE'), port=port, host='0.0.0.0')
