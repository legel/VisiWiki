'''
Created on Feb 5, 2014

@author: homliu
'''
import os
from flask import request
from flask import Flask
from HTMLGetter import *
from web.DoQuery import *
import json
from web.MySQLConnector import *

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './html')

app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)

def read_file(filename):
    f=open(filename)
    text = '\n'.join(f)
    #close(f)
    return text

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hello")
def hello2():
    return "Hello World2!"

@app.route("/about")
def about():
    return "About the page"

@app.route("/post/<username>/<int:post_id>")
def show_post(username,post_id):
    return "username:%s post_id:%d" % (username,post_id)

    
@app.route('/html/<path:filename>')
def send_foo(filename):
    #return read_file('html/'+filename)
    return app.send_static_file('html/'+filename)

queryObj = DoQuery()
Connector = MySQLConnector()

@app.route('/query/<topic>')
def query(topic):
    text = queryObj.query(topic)
    print text
    return json.dumps(text)
    
@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        if request.form.has_key('username') and request.form.has_key('pwd'):
		if Connector.login(request.form['username'],request.form['pwd'])==0:
			return "Login success."
    return "Login failed."

@app.route("/registration", methods = ['POST','GET'])
def registration():
    if request.method == 'POST':
	    if request.form.has_key('username') and request.form.has_key('pwd1') and request.form.has_key('pwd2') and request.form.has_key('email'):
		result=Connector.register(request.form['username'],request.form['pwd1'],request.form['email'])
		if result == -2:
		    return "User already exists."
		if result == -1:
		    return "Password not equal."
	        return "Register success."

if __name__ == "__main__":
    app.debug = True
    #url_for('static', filename = 'hello.html')
    app.run(host='0.0.0.0')
    
    
    
    
    
