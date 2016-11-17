def login():
	if request.method == 'GET':
		return render_template('login.html')


	email = get_field(request, 'email')
	password = get_field(request, 'password')

	if email is None: return jsonify(error='missing email')
	if password is None: return jsonify(error='missing password')

	db_pass = select_query(check_login % email)
	print(db_pass)
	if len(db_pass) == 0: jsonify(error='email not in database')
	if not bcrypt.check_password_hash(db_pass[0][0], password):
		return jsonify(error='incorrect password')

	return jsonify(success=True, user_id=db_pass[0][1])

def new_friend(request):
	user_id1, err = get_num(request, 'user_id1')
	user_id2, err = get_num(request, 'user_id2')

	if err is not None:
		return jsonify(error=err)

	if(user_id1 == user_id2):
		return jsonify(error='cannot befriend self')

	if user_id1 is None or user_id2 is None:
		return jsonify(error='must provide valid user_ids')

	# Verfiy users exist
	resp = select_query(verify_users % user_id1, user_id2)
	if len(resp) != 2:
		return jsonify(error='one or both user_ids do not exist')

	# Verify users not friends
	resp = select_query(check_not_already_friends % (user_id1, user_id2))
	if len(resp) != 0:
		return jsonify(error='users already friends')

	# Add friend
	insert_query(add_friend % (user_id1, user_id2))

	return jsonify(success=True)

def get_friends(request, user_id):
	resp = select_query(view_friends % user_id)
	friends = []
	add_rows_to_list(resp, friends, ('user_id', 'first_name', 'last_name'))

	print(friends)
	if len(friends) == 0:
		ls = ''
	else:
		ls = 'AND NOT (user_id in (%s))' % (','.join([friend.user_id for friend in friends]))
	
	resp = select_query(added_me % (user_id, ls))
	non_friends = []
	add_rows_to_list(resp, non_friends, ('user_id', 'first_name', 'last_name'))

	return Response(json.dumps({'friends':friends, 'non_friends':non_friends}),  mimetype='application/json')

def search_users(request):
	if request.method == 'GET':
		return render_template('search.html')

	query = get_field(request, 'query')
	user_id, err = get_num(request, 'user_id')

	if err is not None:
		return jsonify(error=err)

	if query is None: return jsonify(error='query required')
	if user_id is None: return jsonify(error='user_id required')

	query = query.lower()

	results = []
	# search among friends
	# rows = select_query(search_friends % (user_id, to_name(query), to_name(query), query,  to_name(query), to_name(query)))
	# add_rows_to_list(rows, results, ('user_id', 'first_name', 'last_name', 'email'))

	# search among friends' friends

	# search among all users
	rows = select_query(search_all % (to_name(query), to_name(query), query,  to_name(query), to_name(query)))
	add_rows_to_list(rows, results, ('user_id', 'first_name', 'last_name', 'email'))
	return Response(json.dumps(results), mimetype='application/json')

def new_user(request):
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

	first_name = to_name(first_name)
	last_name = to_name(last_name)
	email = email.lower()

	print('%s\n%s\n%s\n%s\n%s\n%s' % (first_name, last_name, fb_id, email, password.decode('UTF-8')))		
	insert_query(new_user % (first_name, last_name, fb_id, email, password.decode('UTF-8')))

	return jsonify(success=True)

def get_all_users(request):
	query = show_all_users
	response = select_query(query)
	return  Response(json.dumps(response),  mimetype='application/json')

def get_user(request):
	query = show_user % user_id
	response = select_query(query)
	return  Response(json.dumps(response),  mimetype='application/json')