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


app = Flask(__name__)
CORS(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = 'munchr_test'
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_DATABASE_HOST') or 'localhost'
mysql.init_app(app)


# print('Attempting to connect to databse')
# try:
# 	conn = mysql.connect()
# except:
# 	print ("I am unable to connect to the database")
# 	sys.exit(1)
# print ('Connected to database')

conn = None

users = Users(conn, Bcrypt(app))
# socketio = SocketIO(app)


# rooms = {}

@app.route('/restaurants/', methods=['GET','POST'])
def get_restaurants(): 
	if request.method == 'GET':
		return render_template('restaurants.html')
	return restaurants.get_restaurants(request)

@app.route('/restaurants/categories', methods=['GET'])
def get_categories(): 
	return restaurants.get_categories()

@app.route('/restaurants/cuisines', methods=['GET'])
def get_cuisines(): 
	return restaurants.get_cuisines(request)


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	print('request.data: ' + request.data)
	print('request.args: ' + request.args)
	print('request.form: ' + request.form)
	print('request.files: ' + request.files)
	print('request.values: ' + request.values)
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

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == "__main__":
	port = int(os.environ.get('MUNCHR_PORT')) or 5000
	app.run(debug=(os.environ.get('MUNCHR_PROD') != True), port=port, host='0.0.0.0')
    