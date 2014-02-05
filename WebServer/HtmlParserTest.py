
import socket
import urllib2
import re
import sys
from sets import Set
from WikiStats import *
from HTMLGetter import *

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):
    def __init__(self,g):
        self.reset()
        self.start = False
        self.f = open(g,'w')
        self.divCount = 0
    
    def handle_starttag(self, tag, attrs):
        if self.start and tag == 'div':
            self.divCount +=1
            return
        
        for attr in attrs:
            #print "     attr:", attr
            if attr[0] == 'id' and attr[1] =='bodyContent' :
                self.start =True
                self.divCount = 1
                
    def handle_data(self, data):
        if self.start and len(data.strip())!=0:
            #print data
            self.f.write(data)
            self.f.write(' ')
        
    def handle_endtag(self, tag):
        #print "end"
        #print self.divCount
        if self.start and tag == 'div':
            self.divCount -=1
        if self.start and self.divCount == 0:
            self.start = False
            self.f.close()
            #print "false"
        #sprint "End tag  :", tag


if __name__ == '__main__':
    for (dirpath, dirnames, filenames) in walk('./pages2/'):
        for t in filenames:
            f = dirpath+t
            g = './output2/'+t[0:t.find(".gz")]
            print g
            lines=gzip.open(f)
            texts = [line for line in lines.readlines()]
            text = ' '.join(texts).encode('utf-8')
            #print text
            parser = MyHTMLParser(g)
            parser.feed((text))
