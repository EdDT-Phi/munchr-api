from utils.err import InvalidUsage
from utils.db_helper import get_db
from math import radians, cos, sin, asin, sqrt
from datetime import datetime


def haversine(lat1, lon1, lat2, lon2):
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
	if field not in request.form:
		if required:
			raise InvalidUsage('%s is required' % field, status_code=400)
		return None

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
		raise InvalidUsage('%s must be a number' % field, status_code=400)

	if ret > max_num or ret < min_num:
		raise InvalidUsage('%s must be between %d and %d' % (field, min_num, max_num))

	return ret


def get_float(request, field, required=False):
	ret = get_field(request, field, required)
	if ret is None and not required:
		return None

	try:
		ret = float(ret)
	except:
		raise InvalidUsage('%s must be a float' % field, status_code=400)

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


def select_query(query, params=None):
	db = get_db()
	conn = db.getconn()
	cursor = conn.cursor()

	cursor.execute(query, params)
	rows = cursor.fetchall()

	cursor.close()
	conn.close()

	db.putconn(conn)

	return rows


def update_query(query, params=None, fetch=False):
	db = get_db()
	conn = db.getconn()
	cursor = conn.cursor()

	cursor.execute(query, params)
	rows = None
	if fetch:
		rows = cursor.fetchall()

	cursor.close()
	conn.commit()
	conn.close()

	db.putconn(conn)

	return rows


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


def time_to_text(time):
	ago = datetime.now() - time
	if ago.days > 1:
		return '%d days ago' % ago.days
	elif ago.days == 1:
		return 'Yesterday'
	elif ago.seconds >= 60*60:
		hrs = ago.seconds // (60*60)
		sing = 'hour'
		if hrs > 1:
			sing += 's'
		return '%d %s ago' % (hrs, sing)
	elif ago.seconds > 60:
		return 'A few minutes ago'
	else:
		return 'A few seconds ago'
