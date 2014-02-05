'''
Created on Feb 1, 2014

@author: homliu
'''

from HTMLGetter import *
import socket
import urllib2
import re
from sets import Set

timeout = 20
socket.setdefaulttimeout(timeout)

class PageDownloader:
    def __init__(self,fileOfList):
        self.fileOfList = fileOfList
        file = open(fileOfList)
        self.links = []
        self.count =0
        for line in file:
            words = line.split()
            link =words[0]
            self.links.append(link)
            self.count +=1
    
    def process(self,start=0):
        i=-1
        for link in self.links:
            i+=1
            if i<start:
                continue
            pageUrl = 'http://en.wikipedia.org/wiki/' + link
            print "Getting ID=%d %s ..." % (i, pageUrl)
            try:
                obj =  HTMLGetter()
                obj.process(pageUrl)
                obj.save('./pages/'+link)
            except Exception as e:
                pass
            
        
if __name__ == '__main__':
    obj =  PageDownloader('./output/total_stats')
    obj.process(92241)
        
    