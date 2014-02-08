'''
Created on Feb 5, 2014

@author: homliu
'''
import os
import json
from flask import Flask, session, redirect, url_for, escape, request
from HTMLGetter import *
from web.DoQuery import *
from web.MySQLConnector import *

############## initialization #######
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './html')
app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)
queryObj = DoQuery()
Connector = MySQLConnector()

def read_file(filename):
    f=open(filename)
    text = '\n'.join(f)
    #close(f)
    return text


################# home page ###########
@app.route("/")
def root():
    if session.has_key('username'):
        #return send_page('search.html')
        print "User:%s vistiting" % session['username']
        return redirect(url_for('static', filename='search_button.html'))
    else:
        #return send_page('index.html')
        return redirect(url_for('static', filename='login_form.html'))


################# do login ##########
@app.route("/login", methods = ['POST','GET'])
def doLogin():
    if request.method == 'POST':
        if request.form.has_key('username') and request.form.has_key('pwd') and \
           Connector.login(request.form['username'],request.form['pwd'])==0:
                session['username'] = request.form['username']
                return redirect(url_for('static', filename='search_button.html'))
        
    return "Login failed."


@app.route("/registration", methods = ['POST','GET'])
def registration():
    if request.method == 'POST':
        if request.form.has_key('username') and request.form.has_key('pwd1') and \
            request.form.has_key('pwd2') and request.form.has_key('email'):
            result=Connector.register(request.form['username'],request.form['pwd1'],\
                                      request.form['pwd2'],request.form['email'])
            if result == -1:
                return "User already exists."
            if result == -2:
                return "Password not equal."
            
            return redirect(url_for('static', filename='regsuccess.html'))

@app.route('/query/<topic>')
def query(topic):
    jsonText = queryObj.queryJson(topic)
    return jsonText
 

####################################################################
@app.route("/about")
def about():
    return "About the page"

@app.route("/post/<username>/<int:post_id>")
def show_post(username,post_id):
    return "username:%s post_id:%d" % (username,post_id)
    
@app.route('/html/<path:filename>')
def send_page(filename):
    print ('Requesting: html/'+ filename)
    return app.send_static_file('/html/'+filename)

@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.debug = True
    app.secret_key ='zxnvkjnu23909hasdHSDH(PH'
    app.run(host='0.0.0.0')
    
    
    
    
    
