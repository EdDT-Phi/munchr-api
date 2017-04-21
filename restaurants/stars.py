import os
from flask import jsonify, Blueprint, request

from utils import queries, utils


stars_blueprint = Blueprint('stars', __name__)


@stars_blueprint.route('/stars/<int:user_id>',  methods=['GET', 'POST'])
def notifications(user_id):
	if request.method == 'POST':
		res_id = utils.get_field(request, 'res_id', required=True)
		utils.update_query(queries.new_star, (user_id, res_id))
		return jsonify(success=True)

	stars = []
	rows = utils.select_query(queries.get_stars, (user_id,));
	utils.add_rows_to_list(rows, stars, ('res_id', 'res_name'))

	return jsonify(results=stars)


@stars_blueprint.route('/stars/unstar/<int:user_id>/<string:res_id>')
def delete_star(user_id, res_id):
	utils.update_query(queries.delete_star, (user_id, res_id));
	return notifications(user_id)

def is_starred(user_id, res_id):
	check = utils.select_query(queries.check_single_star, (user_id, res_id))
	return len(check) > 0

def get_all_starred(user_id):
	rows = utils.select_query(queries.get_stars, (user_id,))
	return [row[0] for row in rows]

