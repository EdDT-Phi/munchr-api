from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import psycopg2
import json
import pdb
import sys
import requests
import utils

app = Flask(__name__)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

try:
	conn = psycopg2.connect("dbname='letsgo' user='postgres' host='localhost'")
except:
	print ("I am unable to connect to the database")
	sys.exit(1)
print ('Connected to database')



rooms = {}


google_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%d&keyword=%s&minprice=%d&maxprice=%dtype=restaurant&opennow=true&key=AIzaSyAYtekAb_1WMTW3S4VhdylPOBpf1QeNIIo'
radius_conv = {1: 1000, 2: 5000, 3: 10000}

@app.route('/restaurants/', methods=['GET','POST'])
def getRestaurants(): 
	if request.method == 'GET':
		return render_template('restaurants.html')

	return restaurants.get_retaurants(request)


@app.route('/login/', methods=['GET', 'POST'])
def login():
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
	return search_users(request)


@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>')
def users(user_id=None):
	if request.method == 'POST':
		return users.new_user(request)

	if user_id is None:
		return users.get_all_users(request)

	return get_user(request, user_id)


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


if __name__ == '__main__':
    socketio.run(app, debug=True)