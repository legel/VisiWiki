'''
Created on Feb 1, 2014

@author: homliu
'''

import socket
import urllib2
import re
from sets import Set
from WikiStats import *

timeout = 20
socket.setdefaulttimeout(timeout)
linkPattern = re.compile('<a href="(.*?)">(.*?)</a>', re.IGNORECASE)
    
class HTMLGetter:
    def __init__(self):
        pass
    
    def process(self,url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        self.the_page = response.read()
        #print self.the_page
        
    def getPage(self):
        return self.the_page
    
    def save(self,path):
        f = open(path, 'w')
        f.write(self.the_page)
        f.close()
        
    def getLinks(self): #Return the URL in the escaped format
        #m = linkPattern.match( self.the_page)
        result = linkPattern.findall(self.the_page)
        links= Set([])
        for link in result:
            if(link[0].startswith('/wiki/') and not link[1].startswith("<")):
                end=link[0].find("\"")
                links.add(link[0][6:end])
                #links.add(link[1])
        #for link in links:
        #    print link
        print "Size:%d" %( len(links) )
        return links

class LinkParser:
    def __init__(self):
        self.stats =  TotalStatsParser()
        self.stats.setDataSource('./output/total_stats')
        self.dicts= self.stats.process()
    
    def lookup(self,topic):
        obj =  HTMLGetter()
        obj.process('http://en.wikipedia.org/wiki/'+topic)
        links = obj.getLinks()
        #print links
        filterLinks = []
        for link in links:
            count = self.dicts.get(link,0)
            if count > 0:
                filterLinks.append(LinkStat(link,count))
        filterLinks.sort(key = lambda x : int(x.count), reverse=True)
        return filterLinks
        

if __name__ == '__main__':
    obj =  HTMLGetter()
    obj.process('http://en.wikipedia.org/wiki/Computer_science')
    links = obj.getLinks()
    
    obj2 =  TotalStatsParser()
    obj2.setDataSource('./output/total_stats')
    dicts= obj2.process()
    
    
    filterLinks = []
    for link in links:
        count = dicts.get(link,0)
        if count > 0:
            filterLinks.append(LinkStat(link,count))
    
    filterLinks.sort(key = lambda x : int(x.count), reverse=True)
    
    for link in filterLinks:
        print link
        
    