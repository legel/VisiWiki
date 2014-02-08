import mysql.connector

cnx = mysql.connector.connect(user='', password='',
                              host='127.0.0.1',
                              database='test')

cursor = cnx.cursor()

query = 'select * from test'

cursor.execute(query)

for (first_name) in cursor:
    print first_name

cursor.close()


cnx.close()