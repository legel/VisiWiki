import mysql.connector
import hashlib

class MySQLConnector:
	def __init__(self):
		self.conn = mysql.connector.connect(host='127.0.0.1', user='', passwd='',database='test')
		self.cursor = self.conn.cursor()
	def __del__(self):
		self.cursor.close()
		self.conn.close()
	
	def InitDB(self):
		queries = (
			"create table user ("
			" username varchar(20) NOT NULL,"
			" pswd varchar(50) NOT NULL,"
			" email varchar(30) NOT NULL,"
			" primary key (username)"
			" ) ENGINE=InnoDB")
		self.cursor.execute(queries)

		queries = (
			"create table history ("
			" id bigint NOT NULL,"
			" username varchar(20) NOT NULL,"
			" page varchar(20) NOT NULL,"
			" time datetime NOT NULL,"
			" IP varchar(16) NOT NULL,"
			" primary key (id)"
			" ) ENGINE=InnoDB")
		self.cursor.execute(queries)
		self.conn.commit()

	def login(self, uname, pswd):
		H=hashlib.sha1(pswd).hexdigest()
		queries = (
			"SELECT pswd from user "
			"where username = %s")
		self.cursor.execute(queries,(uname))
		for stored_pswd in self.cursor:
			if stored_pswd[0] != H:
				return -1
			else:
				return 0
		return -2
	
	def register(self, uname, pswd1, pswd2, email):
		H1=hashlib.sha1(pswd1).hexdigest()
		H2=hashlib.sha1(pswd2).hexdigest()
		if H1 != H2:
			return -2

		queries = (
			"SELECT * from user "
			"where username = %s")
		self.cursor.execute(queries, (uname))
		for _ in self.cursor:
			return -1
		queries = (
			"INSERT into user "
			"(username, pswd, email)"
			"values (%s, %s,%s)")

		self.cursor.execute(queries,(uname,H1,email))
		self.conn.commit()
		return 0

	def visit(self, uname, page, time, IP):
		queries = (
			"SELECT count(*) from history")
		self.cursor.execute(queries)
		ID=self.cursor.fetchall()[0][0]+1
		queries = (
			"insert into history"
			"(id, username, page,time,IP)"
			"values (%s, %s, %s, %s, %s)")
		self.cursor.execute(queries,(ID,uname,page,time,IP))
		self.conn.commit()
