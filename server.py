import os
import json

from flask import Flask, jsonify, render_template
from flask_cors import CORS

from users.users import users_blueprint
from users.friends import friends_blueprint
from users.ratings import ratings_blueprint
from restaurants.restaurants import restaurants_blueprint
from restaurants.restaurants_qa import restaurants_qa_blueprint
from restaurants.recommendations import recommendations_blueprint
from restaurants.stars import stars_blueprint
from utils import utils
from utils.err import InvalidUsage

app = Flask(__name__)
CORS(app)

app.register_blueprint(restaurants_blueprint)
app.register_blueprint(restaurants_qa_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(friends_blueprint)
app.register_blueprint(ratings_blueprint)
app.register_blueprint(recommendations_blueprint)
app.register_blueprint(stars_blueprint)


@app.route('/')
def hello_world():
	return render_template('landing.html')

@app.route('/restaurants/<string:res_id>')
def hello_res(res_id):
    return render_template('restaurant.html')


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    print('An error occurred during a request.')
    print(e)
    return jsonify(error='An internal error occurred.'), 500


if __name__ == "__main__":
    port = int(os.environ.get('MUNCHR_PORT') or 5000)
    app.run(debug=(os.environ.get('DEBUG') == 'true'), port=port, host='0.0.0.0')
