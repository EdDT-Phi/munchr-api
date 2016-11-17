def get_field(request, field):
	ret = request.form[field]
	if ret == '': return None
	return ret


def get_num(request, field, min=0, max=1000000):
	ret = get_field(request, field)
	try:
		ret = int(ret)
	except:
		return (None, '%s must be a number' % field)

	if ret > max or ret < min:
		return (None, '%s must be between %d and %d' % (field, min, max))

	return (ret, None)


def select_query(query):
	cursor = conn.cursor()
	cursor.execute(query)
	rows = cursor.fetchall()
	cursor.close()
	return rows

def insert_query(query):
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