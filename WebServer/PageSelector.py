'''
Created on Feb 1, 2014

@author: homliu
'''

from HTMLGetter import *
import socket
import urllib2
import re
from sets import Set
import os

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
            count = int(words[1])
            self.links.append(link)
            #print count
            if count>10000:
                self.count +=1
                file = './pages/%s.gz' % (link)
                dest = './pages2/%s.gz' % (link)
                try:
                    #os.rename(file, dest)
                    print file
                except:
                    pass
        print self.count
    
    def process(self,start=0):
        i=-1
        for link in self.links:
            i+=1
            if i<start:
                continue
            pass
            
        
if __name__ == '__main__':
    obj =  PageDownloader('./output/total_stats')
    obj.process()
        
    