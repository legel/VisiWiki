import mysql.connector
import hashlib
import datetime
import sys

class MySQLConnector:
	def __init__(self):
		self.conn = mysql.connector.connect(host='127.0.0.1', user='', passwd='',database='test')
		self.cursor = self.conn.cursor()
		self.cursor.execute('use test')
		
	def __del__(self):
		self.cursor.close()
		self.conn.close()
	
	def InitDB(self):
		try:
			queries = (
				"create table user ("
				" username varchar(32) NOT NULL,"
				" pswd varchar(50) NOT NULL,"
				" email varchar(30) NOT NULL,"
				" primary key (username)"
				" ) ENGINE=InnoDB ")
			self.cursor.execute(queries)
			queries = ( "create index userIdx  on user(username, email)")
			self.cursor.execute(queries)
		except Exception:
			print "error with user table"
			pass

		try:
			queries = (
				"create table history ("
				" username varchar(32) NOT NULL,"
				" page varchar(256) NOT NULL,"
				" time datetime NOT NULL,"
				" IP varchar(16) NOT NULL"
				" ) ENGINE=InnoDB ")
			self.cursor.execute(queries)
			queries = ( "create index historyIdx on history(username, page, time)")
			self.cursor.execute(queries)
		except Exception:
			print "error with history table"
			pass
		
		self.conn.commit()

	def InitLDADB(self):
		try:
			self.cursor.execute("create table ldaArticleMap ( article_id int, article_name varchar(256))")
			self.cursor.execute("create table ldaArticleTopicMap (article_id int, topic_id int, weight double, article_list int)")
			self.cursor.execute("create table ldaTopicToArticle ( topic_id int, article_id int, order_id int)")
			self.cursor.execute("create index ldaArticleMapIdx on ldaArticleMap(article_name,article_id)")
			self.cursor.execute("create index ldaArticleTopicMapIdx on ldaArticleTopicMap(article_id,topic_id)")
			self.cursor.execute("create index ldaTopicToArticle on ldaTopicToArticle(topic_id,article_id)")
		except Exception:
			print "error with lda table"
			print sys.exc_info()[0]
			pass
		
		self.conn.commit()
		
	def login(self, uname, pswd):
		H=hashlib.sha1(pswd).hexdigest()
		queries = (
			"SELECT pswd from user where username = %s")
		self.cursor.execute(queries,[uname])
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
			"SELECT pswd from user where username = %s")
		self.cursor.execute(queries, [uname])
		for _ in self.cursor:
			print _
			return -1
		queries = (
			"INSERT into user "
			"(username, pswd, email)"
			"values (%s, %s, %s)")

		self.cursor.execute(queries,(uname,H1,email))
		self.conn.commit()
		return 0

	def visit(self, uname, page, time, IP):
		queries = (
			"insert into history"
			"(username, page,time,IP)"
			"values ( %s, %s, %s, %s)")
		self.cursor.execute(queries,[uname,page,time,IP])
		self.conn.commit()

	def insertLDAMapping(self, article_id, topic_id, weight, article_lists):
		queries = (
			"insert into ldaArticleTopicMap"
			"(article_id , topic_id , weight , article_list )"
			"values ( %s, %s, %s, %s)")
		self.cursor.execute(queries,[article_id,topic_id,weight,topic_id])
		for f in self.cursor:
			pass
		
		queries = ("select * from ldaTopicToArticle where topic_id = %s")
		self.cursor.execute(queries,[topic_id])
		size =0
		for r in self.cursor:
			size +=1
		
		if(size ==0):
			i = 0
			for l in article_lists:
				queries = ("insert into ldaTopicToArticle (topic_id, article_id, order_id ) values (%s, %s, %s)" )
				self.cursor.execute(queries,[topic_id, l, i])
				for f in self.cursor:
					pass
				i += 1
				
		self.conn.commit()
		
	def commit(self):
		self.conn.commit()
		
		
if __name__ == '__main__':
	obj = MySQLConnector()
	obj.InitDB()
	obj.InitLDADB()
	#obj.visit('a', 'CS', datetime.datetime.now(), '0.0.0.0');
