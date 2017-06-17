import os
from flask import jsonify, Blueprint, request

from utils import queries, utils
from auth import auth

stars_blueprint = Blueprint('stars', __name__)


@stars_blueprint.route('/stars/',  methods=['POST'])
@auth.login_required
def get_stars():

	user_id = utils.get_num(request, 'user_id', required=True)

	stars = []
	rows = utils.select_query(queries.get_stars, (user_id,));
	utils.add_rows_to_list(rows, stars, ('res_id', 'res_name', 'photo_url'))

	return jsonify(results=stars)


@stars_blueprint.route('/stars/new/', methods=['POST'])
@auth.login_required
def new_star():

	user_id = utils.get_num(request, 'user_id', required=True)
	res_id = utils.get_field(request, 'res_id', required=True)

	utils.update_query(queries.new_star, (user_id, res_id))
	return jsonify(success=True)


@stars_blueprint.route('/stars/unstar/' , methods=['POST'])
@auth.login_required
def delete_star():

	user_id = utils.get_num(request, 'user_id', required=True)
	res_id = utils.get_field(request, 'res_id', required=True)

	utils.update_query(queries.delete_star, (user_id, res_id))
	return notifications(user_id)


def is_starred(user_id, res_id):

	check = utils.select_query(queries.check_single_star, (user_id, res_id))
	return len(check) > 0


def get_all_starred(user_id):

	rows = utils.select_query(queries.get_stars, (user_id,))
	return [row[0] for row in rows]

