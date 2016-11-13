from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_socketio import SocketIO
import psycopg2
import json
import pdb
import sys
import requests

app = Flask(__name__)
bcrypt = Bcrypt(app)

try:
	conn = psycopg2.connect("dbname='letsgo' user='postgres' host='localhost'")
except:
	print ("I am unable to connect to the database")
	sys.exit(1)
print ('Connected to database')


google_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%d&keyword=%s&minprice=%d&maxprice=%dtype=restaurant&opennow=true&key=AIzaSyAYtekAb_1WMTW3S4VhdylPOBpf1QeNIIo'

lat = '30.287235'
lng = '-97.744111'
rad = 2
kwrd = 'burgers'
minprice = 0
maxprice = 4

radius_conv = {1: 1000, 2: 5000, 3: 10000}

@app.route('/restaurants/', methods=['GET','POST'])
def getRestaurants(): 
	if request.method == 'GET':
		return render_template('restaurants.html')

	lat = get_field(request, 'lat')
	lng = get_field(request, 'long')
	rad, err = get_num(request, 'radius', 1, 3)
	kwrd = get_field(request, 'keyword')
	min_price, err = get_num(request, 'min_price', 0, 4)
	max_price , err = get_num(request, 'max_price', min_price, 4)
	user_id, err = get_num(request, 'user_id')

	if err is not None:
		return jsonify(error=err)
	
	if lat is None: return jsonify(error='missing lat')
	if lng is None: return jsonify(error='missing long')
	if rad is None: return jsonify(error='missing radius')
	if min_price is None: return jsonify(error='missing min_price')
	if max_price is None: return jsonify(error='missing max_price')
	if user_id is None: return jsonify(error='missing user_id')

	rad = radius_conv[rad] 
	resp = requests.get(google_url % (lat, lng, rad, kwrd, min_price, max_price))
	data = resp.json()
	print(data)
	return jsonify(**data)

check_login = 'SELECT password, user_id FROM users WHERE email = \'%s\''

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')


	email = get_field(request, 'email')
	password = get_field(request, 'password')

	if email is None: return jsonify(error='missing email')
	if password is None: return jsonify(error='missing password')

	cursor = conn.cursor()
	cursor.execute(check_login % email)
	
	db_pass = cursor.fetchall()
	print(db_pass)
	if len(db_pass) == 0: jsonify(error='email not in database')
	if not bcrypt.check_password_hash(db_pass[0][0], password):
		return jsonify(error='incorrect password')

	return jsonify(success=True, user_id=db_pass[0][1])


verify_users = 'SELECT user_id FROM users WHERE user_id=%d OR user_id=%d'
check_not_already_friends = 'SELECT user_id1, user_id2 FROM friends WHERE user_id1=%d AND user_id2=%d'
add_friend = 'INSERT INTO friends (user_id1, user_id2) VALUES (%d, %d)'
view_friends = 'SELECT user_id, first_name, last_name FROM friends JOIN users ON user_id = user_id2 WHERE user_id1 = %d'
added_me = 'SELECT user_id, first_name, last_name FROM friends JOIN users ON user_id = user_id1 WHERE user_id2 = %d %s'

@app.route('/friends/', methods=['GET', 'POST'])
@app.route('/friends/<int:user_id>')
def friends(user_id=None):

	if user_id is None and request.method == 'GET':
		return render_template('new_friend.html')

	if request.method == 'POST':
		user_id1, err = get_num(request, 'user_id1')
		user_id2, err = get_num(request, 'user_id2')

		if err is not None:
			return jsonify(error=err)

		if(user_id1 == user_id2):
			return jsonify(error='cannot befriend self')

		if user_id1 is None or user_id2 is None:
			return jsonify(error='must provide valid user_ids')

		# Verfiy users exist
		cursor = conn.cursor()
		query = verify_users % (user_id1, user_id2)
		cursor.execute(query)
		resp = cursor.fetchall()
		if len(resp) != 2:
			cursor.close()
			return jsonify(error='one or both user_ids do not exist')

		# Verify users not friends
		query = check_not_already_friends % (user_id1, user_id2)
		cursor.execute(query)
		resp = cursor.fetchall()
		if len(resp) != 0:
			cursor.close()
			return jsonify(error='users already friends')

		# Add friend
		query = add_friend % (user_id1, user_id2)
		cursor.execute(query)
		cursor.close()
		conn.commit()

		return jsonify(success=True)

	cursor = conn.cursor()
	query = view_friends % user_id
	cursor.execute(query)
	resp = cursor.fetchall()

	friends = []
	ls = 'AND NOT (user_id in ('
	for user in resp:
		ls += str(user[0]) + ','
		friends.append({'user_id': user[0], 'first_name': user[1], 'last_name': user[2]})

	ls = ls[:len(ls)-1] + '))'

	if len(friends) == 0:
		ls = ''
	query = added_me % (user_id, ls)
	cursor.execute(query)
	resp = cursor.fetchall()
	cursor.close()

	non_friends = []
	for user in resp:
		non_friends.append({'user_id': user[0], 'first_name': user[1], 'last_name': user[2]})

	return Response(json.dumps({'friends':friends, 'non_friends':non_friends}),  mimetype='application/json')

search_query = ''

@app.route('/users/search/<string:query>')
def users_search(query):
	# seach among friends
	# search among friends freinds
	# search among all users


new_user = 'INSERT INTO users (first_name, last_name, fb_id, email, password) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'
show_all_users = 'SELECT * from users ORDER BY user_id DESC'
show_user = 'SELECT * from users WHERE user_id = %d'

@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>')
def users(user_id=None):
	if request.method == 'POST':

		first_name = get_field(request, 'first_name')
		last_name = get_field(request, 'last_name')
		fb_id = get_field(request, 'fb_id')
		email = get_field(request, 'email')
		password = get_field(request, 'password')

		if first_name is None: return jsonify(error='first_name required')
		if last_name is None: return jsonify(error='last_name required')
		if email is None: return jsonify(error='email required')
		if password is None: 
			if fb_id is None: return jsonify(error='password or fb_id required')
		else:
			password = generate_password_hash(password, 12)

		print('%s\n%s\n%s\n%s\n%s' % (first_name, last_name, fb_id, email, password.decode('UTF-8')))
		
		try:
			cursor = conn.cursor()
			query = new_user % (first_name, last_name, fb_id, email, password.decode('UTF-8'))
			cursor.execute(query)
			cursor.close()
			conn.commit()
		except:
			print("FAILED TO ADD USER")
			raise

		return jsonify(success=True)


	query = show_all_users
	if user_id is not None:
		query = show_user % user_id	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		response = cursor.fetchall()
		cursor.close()
	except:
		print ("FAILED TO GET USERS")
		raise

	return  Response(json.dumps(response),  mimetype='application/json')



@app.route('/users/new')
def newUser():
	return render_template('new_user.html')


def get_field(request, field):
	ret = request.form[field]
	if ret == '': return None
	return ret

def get_num(request, field, min=0, max=1000000):
	ret = get_field(request, field)
	try:
		ret = int(ret)
	except:
		return (None, '%s must be a number' % field)

	if ret > max or ret < min:
		return (None, '%s must be between %d and %d' % (field, min, max))

	return (ret, None)


if __name__ == '__main__':
	app.run()