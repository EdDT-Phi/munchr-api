from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
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
# TODO get rid of plaintext password
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD') or '3sV#GH@jB6C}$cuh'
app.config['MYSQL_DATABASE_DB'] = 'munchr_test'
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_DATABASE_HOST') or 'localhost'
mysql.init_app(app)


print('Attempting to connect to databse')
try:
	conn = mysql.connect()
except:
	print ("I am unable to connect to the database")
	raise
	sys.exit(1)
print ('Connected to database')

users = Users(conn, Bcrypt(app))
socketio = SocketIO(app)


# rooms = {}

@app.route('/restaurants/', methods=['GET','POST'])
def getRestaurants(): 
	if request.method == 'GET':
		return render_template('restaurants.html')

	return restaurants.get_restaurants(request)


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


@socketio.on('my_ping', namespace='/session')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/session')
def test_connect():
    print('connect')
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('connect_join', namespace='/session')
def test_message(message):
    print('connect_join')
    # session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': 420})


@app.route('/users/new')
def newUser():
	return render_template('new_user.html')


@app.route('/session/create')
def create():
	return render_template('create_session.html')


@app.route('/session/join')
def join():
	return render_template('join.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    socketio.run(app, debug=True)
    