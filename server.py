from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL
import json
import pdb
import sys
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
		return render_template('restaurants.html')
	return restaurants.get_restaurants(request)


@app.route('/restaurants/filters', methods=['POST'])
def get_filters():
	return restaurants.get_filters(request)


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	return users.login(request)


@app.route('/friends/', methods=['GET', 'POST'])
@app.route('/friends/<int:user_id>')
def friends(user_id=None):
	if user_id is None and request.method == 'GET':
		return render_template('new_friend.html')

	if request.method == 'POST':
		return users.new_friend(request)

	return users.get_friends(request, user_id)


@app.route('/users/search/', methods=['GET', 'POST'])
def users_search():
	if request.method == 'GET':
		return render_template('search.html')
	return users.search_users(request)


@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>')
def users_route(user_id=None):
	if request.method == 'POST':
		return users.new_user(request)

	if user_id is None:
		return users.get_all_users(request)

	return users.get_user(request, user_id)


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
	app.run(debug=(os.environ.get('MUNCHR_PROD') != True), port=port, host='0.0.0.0')
