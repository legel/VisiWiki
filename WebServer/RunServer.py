'''
Created on Feb 5, 2014

@author: homliu
'''
import os
from flask import request
from flask import Flask
from HTMLGetter import *
app = Flask(__name__)

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
    return read_file('html/'+filename)
    #app.send_static_file(os.getcwd() +'html/index.html')

parser = LinkParser()

@app.route('/query/<topic>')
def query(topic):
    list = parser.lookup(topic)
    print len(list)
    text = []
    for l in list:
        text.append("<a href='/query/%s'>%s %d</a>" %(l.name,l.name,l.count))
        #text.append(l.name+" "+str(l.count))
    return '<br>'.join(text)
    #app.send_static_file(os.getcwd() +'html/index.html')

@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        print request.form
        if request.form['firstname'] =='tom':
            return "welcome, %s " % (request.form['firstname'])
    return "Login failed."

if __name__ == "__main__":
    app.debug = True
    #url_for('static', filename = 'hello.html')
    app.run(host='0.0.0.0')
    
    
    
    
    