import psycopg2
import sys

try:
	conn = psycopg2.connect("dbname='letsgo' user='postgres' host='localhost'")
except:
	print ("I am unable to connect to the database")
	sys.exit(1)
print ('Connected to database')


