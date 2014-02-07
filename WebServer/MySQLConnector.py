import mysql.connector
import hashlib

class Connector:
	def __init__(self):
		self.conn = mysql.connector.connect(host='127.0.0.1', user='', passwd='',database='server')
		self.cursor = self.conn.cursor()
	
	def InitDB(self):
		queries = (
			"create table 'user' ("
			" 'username' varchar(20) NOT NULL,"
			" 'pswd' varchar(50) NOT NULL,"
			" primary key ('username')"
			" ) ENGINE=InnoDB")
		cursor.execute(queries)

		queries = (
			"create table 'history' ("
			" 'id' bigint NOT NULL,"
			" 'username' varchar(20) NOT NULL,"
			" 'page' varchar(20) NOT NULL,"
			" 'time' datetime NOT NULL,"
			" 'IP' varchar(16) NOT NULL,"
			" primary key ('id')"
			" ) ENGINE=InnoDB")
		cursor.execute(queries)

	def login(self, uname, pswd):
		H=hashlib.sha1(pswd).hexdigest()
		queries = (
			"SELECT pswd from user "
			"where username = %s")
		cursor.excute(query,(uname))
		for stored_pswd in cursor:
			if store_pswd != H:
				return false
			else:
				return true
	
	def register(self, uname, pswd1, pswd2):
		H1=hashlib.sha1(pswd1).hexdigest()
		H2=hashlib.sha1(pswd2).hexdigest()
		if H1 != H2:
			return -2

		queries = (
			"INSERT into user "
			"(username, pswd)"
			"values (%s, %s)")

		cursor.execute(queries,(uname,pswd1))

