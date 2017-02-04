# from server import conn

def get_field(request, field, required=False):
	try:
		ret = request.form[field]
		if ret == '':
			print('Empty %s' % field)
			return None, ('%s is required' % field if required else None)
		return ret, None
	except:
		print('Missing %s' % field)
		return None, ('%s is required' % field if required else None)


def get_num(request, field, min=0, max=1000000, required=False):
	ret, err = get_field(request, field, required)
	if err is not None: return ret, err
	if ret is None and not required: return None, None

	try:
		ret = int(ret)
	except:
		return (None, '%s must be a number' % field)

	if ret > max or ret < min:
		return (None, '%s must be between %d and %d' % (field, min, max))

	return (ret, None)

def get_boolean(request, field, required=False):
	ret, err = get_field(request, field, required)
	if err is not None: return ret, err
	if ret is None and not required: return None, None

	ret = ret.lower()
	if ret == 'true':
		return True, None
	if ret == 'false':
		return False, None

	return None, '%s must be true or false'


def select_query(query, conn):
	cursor = conn.cursor()
	cursor.execute(query)
	rows = cursor.fetchall()
	cursor.close()
	return rows

def insert_query(query, conn):
	cursor = conn.cursor()
	cursor.execute(query)
	cursor.close()
	conn.commit()

def modify_query(query, conn):
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
	query = query.split(' ')
	for q in query:
		q = to_name(q)
	return ' '.join(query)
