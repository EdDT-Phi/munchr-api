import utils

def get_restaurants():
	lat, err = utils.get_field(request, 'lat', required=True)
	lng, err = utils.get_field(request, 'long', required=True)
	rad, err = utils.get_num(request, 'radius', 1, 3, required=True)
	kwrd, err = utils.get_field(request, 'keyword', required=True)
	min_price, err = utils.get_num(request, 'min_price', 0, 4, required=True)
	max_price, err = utils.get_num(request, 'max_price', min_price, 4, required=True)
	user_id, err = utils.get_num(request, 'user_id', required=True)

	if err is not None:
		return jsonify(error=err)

	rad = radius_conv[rad]
  # call google api
	resp = requests.get(google_url % (lat, lng, rad, kwrd, min_price, max_price))
	data = resp.json()
	return jsonify(**data)

def swipe_restaurant():
  liked, err = utils.get_boolean(request, 'liked', required=True)
  restaurant_id, err = utils.get_num(request, 'restaurant_id', required=True)
  user_id, err = utils.get_num(request, 'user_id', required=True)

  if err is not None:
    return jsonify(error=err)

  resp = utils.modify_query(swipe_restaurant % ())
  return jsonify(success=True)


def rate_restaurant():
  restaurant_id, err = utils.get_num(request, 'restaurant_id', required=True)
  user_id, err = utils.get_num(request, 'user_id', required=True)
  overall_rating, err = utils.get_num(request, 'overall_rating', 1, 5, required=True)
  food_rating, err = utils.get_num(request, 'food_rating'1, 5)
  value_rating, err = utils.get_num(request, 'value_rating'1, 5)
  service_rating, err = utils.get_num(request, 'service_rating'1, 5)
  location_rating, err = utils.get_num(request, 'location_rating'1, 5)
  atmosphere_rating, err = utils.get_num(request, 'atmosphere_rating'1, 5)

  if err is not None:
    return jsonify(error=err)

  resp = utils.modify_query(rate_restaurant % ())
  return jsonify(success=True)
>>>>>>> 17be64a1f846afc05742e6989f823e7e023326e2
