from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from flask_bcrypt import Bcrypt, generate_password_hash
import psycopg2
import json
import pdb

app = Flask(__name__)
bcrypt = Bcrypt(app)

try:
    conn = psycopg2.connect("dbname='letsgo' user='postgres' host='localhost'")
    #password='dbpass'
except:
    print ("I am unable to connect to the database")
    sys.exit(1)


print ('Connected to database')

def getRestaurants(): pass
	# w.Header().Set('Content-Type', 'application/json')
	# fmt.Fprintf(w, '{response: \'Hi there, I love %s!\'}', r.URL.Path[len('/restaurants/'):])

check_login = 'SELECT password FROM users WHERE email = \'%s\''

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')


	user_name = request.form['email']
	if user_name == '': return jsonify(error='missing username')
	password = request.form['password']
	# if password == '': return jsonify(error='missing password')

	cursor = conn.cursor()
	cursor.execute(check_login % user_name)
	
	db_pass = cursor.fetchall()
	if len(db_pass) == 0: jsonify(error='email not in database')
	if not bcrypt.check_password_hash(db_pass[0][0], password):
		return jsonify(error='incorrect password')

	return jsonify(success=True)

new_user = 'INSERT INTO users (first_name, last_name, fb_id, email, password) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'
show_all_users = 'SELECT * from users ORDER BY user_id DESC'
show_user = 'SELECT * from users WHERE user_id = %d'

@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>')
def users(user_id = None):
	if request.method == 'POST':
		first_name = request.form['first_name']
		if first_name == '': return jsonify(error='first_name required')
		last_name = request.form['last_name']
		if last_name == '': return jsonify(error='last_name required')
		fb_id = request.form['fb_id']
		email = request.form['email']
		if email == '': return jsonify(error='email required')
		password = request.form['password']
		if password == '' and fb_id == '': return jsonify(error='password required')
		password = generate_password_hash(password, 12)

		print('%s\n%s\n%s\n%s\n%s' % (first_name, last_name, fb_id, email, password.decode('UTF-8')))
		
		try:
			cursor = conn.cursor()
			query = new_user % (first_name, last_name, fb_id, email, str(password.decode('UTF-8')))
			cursor.execute(query)
			conn.commit()
			cursor.close()
		except:
			print("FAILED TO ADD USER")
			raise

		return jsonify(success=True)


	query = show_all_users
	if user_id != None:
		query = show_user % user_id	
	cursor = conn.cursor()
	try:
	    cursor.execute(query)
	except:
	    print ("FAILED TO GET USERS")
	    raise

	response = cursor.fetchall()
	cursor.close()
	return  Response(json.dumps(response),  mimetype='application/json')

@app.route('/users/new')
def newUser():
	return render_template('new_user.html')

# func main() {
# 	var err error
#     db, err = sqlx.Connect('postgres', 'user=postgres dbname=letsgo sslmode=disable')
#     if err != nil {
#         log.Fatalln(err)
#     }
#     _ = db
#     // db.MustExec(schema)

# 	http.HandleFunc('/restaurants/', getRestaurants)
# 	http.HandleFunc('/users/new/', newUser)
# 	http.HandleFunc('/users/save/', saveUser)
# 	http.HandleFunc('/users/viewAll/', viewAllUsers)
# 	http.Handle('/login/', http.StripPrefix('/login/', http.FileServer(http.Dir('./'))))
# 	http.ListenAndServe(':8080', nil)
# }


# DROP TABLE users;
# CREATE TABLE users (
# 	user_id		serial,
# 	fb_id		text,
#     first_name 	text,
#     last_name 	text,
#     user_name	text,
#     email 		text
# );

# DROP TABLE place;
# CREATE TABLE place (
# 	place_id	serial,
#     name 		text,
#     lat 		float,
#     long 		float
# );

# DROP TABLE likes;
# CREATE TABLE likes (
# 	user_id		uuid,
# 	place_id	uuid,
# 	swipe		boolean,
# 	liked 		boolean,
# 	rating		int,
# 	times		int
# )`

if __name__ == '__main__':
	app.run()