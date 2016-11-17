def get_restaurants():
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