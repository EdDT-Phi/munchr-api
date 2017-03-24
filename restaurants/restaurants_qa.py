from flask import Blueprint, render_template, request
from utils import queries, utils
from restaurants.restaurants import get_details_obj
from restaurants.filters import filters

restaurants_qa_blueprint = Blueprint('restaurants_qa', __name__)


@restaurants_qa_blueprint.route('/restaurants/cuisines/qa', methods=['GET', 'POST'])
def qa_restaurants():
	if request.method == 'POST':
		c1 = utils.get_field(request, 'cuisine_1', required=True)
		c2 = utils.get_field(request, 'cuisine_2')
		c3 = utils.get_field(request, 'cuisine_3')
		res_id = utils.get_field(request, 'res_id')
		cuisines = c1
		if c2 != 'None':
			cuisines += '|%s' % c2
		if c3 != 'None':
			cuisines += '|%s' % c3

		utils.update_query(queries.update_cuisines, (cuisines, res_id, ))

	res_id = utils.select_query(queries.null_cuisines)
	if len(res_id) == 0:
		return 'All Done!'
	return render_template('cuisine_selection.html', data=get_details_obj(res_id[0][0]), filters=filters, res_id=res_id[0][0])
