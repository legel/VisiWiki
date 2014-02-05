'''
Created on Feb 1, 2014

@author: homliu
'''

import socket
import urllib2
import re
from sets import Set
from WikiStats import *
from HTMLGetter import *

timeout = 20
socket.setdefaulttimeout(timeout)
textPattern = re.compile('<.*>(.*?)</.*>', re.IGNORECASE)
    
class Html2Text:
    def __init__(self):
        pass
    
    
if __name__ == '__main__':
    obj =  HTMLGetter()
    obj.process('http://en.wikipedia.org/wiki/Computer_science')
    html = obj.getPage()
    result = textPattern.findall(html)
    for r in result:
        if r != None and len(r.strip()) > 0:
            print r
    

    
    
    