from err import InvalidUsage
from db_helper import get_db
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return round(km * 1.6,2)


def get_field(request, field, required=False):
	if required and (field not in request.form):
		raise InvalidUsage('%s is required' % field, status_code=400)

	ret = request.form[field]
	if required and (ret == '' or ret is None):
		raise InvalidUsage('%s is required' % field, status_code=400)
	return ret


def get_list(request, field, required=False):
	ret = get_field(request, field, required)
	if ret is None or ret == '':
		return None
	return ret.split(',')


def get_num(request, field, min_num=0, max_num=1000000, required=False):
	ret = get_field(request, field, required)
	if ret is None and not required:
		return None

	try:
		ret = int(ret)
	except:
		return InvalidUsage('%s must be a number' % field, status_code=400)

	if ret > max_num or ret < min_num:
		return InvalidUsage('%s must be between %d and %d' % (field, min_num, max_num))

	return ret


def get_boolean(request, field, required=False):
	ret = get_field(request, field, required)
	if ret is None:
		return ret

	ret = ret.lower()
	if ret == 'true':
		return True
	if ret == 'false':
		return False

	return InvalidUsage('%s must be true or false' % field)


def select_query(query):
	db = get_db()
	conn = db.getconn()
	cursor = conn.cursor()
	cursor.execute(query)
	rows = cursor.fetchall()
	cursor.close()
	return rows


def insert_query(query):
	db = get_db()
	conn = db.getconn()
	cursor = conn.cursor()
	cursor.execute(query)
	cursor.close()
	conn.commit()


def modify_query(query):
	db = get_db()
	conn = db.getconn()
	cursor = conn.cursor()
	cursor.execute(query)
	cursor.close()
	conn.commit()


def add_rows_to_list(rows, lst, values):
	for row in rows:
		obj = {}
		for i in range(len(row)):
			obj[values[i]] = row[i]
		lst.append(obj)


def to_name(name):
	return name[0].upper() + name[1:].lower()


def full_name(query):
	query = [to_name(name) for name in query.split(' ')]
	return ' '.join(query)
