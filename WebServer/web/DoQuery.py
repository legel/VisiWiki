'''
Created on Feb 6, 2014

@author: homliu
'''
from HTMLGetter import *
import json
from web.MySQLConnector import *

mysql = MySQLConnector()

class DoQuery(object):

    def __init__(self):
        self.parser = LinkParser()
    
    def query(self, word):
        list = self.parser.lookup(word)
        list.sort(key = lambda x : int(x.count), reverse=True)
        
        topList = []
        i =0
        for l in list:
            topList.append(l)
            i+=1
            if(i==1000):
                break
        return topList
    
    def queryJson(self,word):
        #result = mysql.queryWordInDB(word)
        #print result
        #if result != None:
        #    return result;
        
        links = self.query(word)
        size = len(links)
        groupNum = 3
        chunkSize = size/groupNum
        if(size ==0 or chunkSize==0):
            return ""
        groupID = 0
        idx = 1
        
        maxCount =0
        for link in links:
            maxCount =max(maxCount, link.count)
            
        topicGroup = []
        currentGroup = []
        topicGroup.append({'articles' : currentGroup})
        topicGroup[groupID]['id']=groupID
        groupWeight =0
        for link in links:
            if(idx%chunkSize ==0):
                topicGroup[groupID]['weight']=groupWeight
                topicGroup.append({})
                groupID+=1
                topicGroup[groupID]['articles']= []
                topicGroup[groupID]['id' ]=groupID
                groupWeight=0
            idx += 1
            groupWeight += link.count*100/maxCount 
            topicGroup[groupID]['articles'].append({'id' : idx,\
                                       'name': link.name , \
                                       'url': 'en.wikipedia.org/wiki/'+ link.name , \
                                       'weight': link.count*100/maxCount  });
        
        topicGroup[groupID]['weight']=groupWeight
        return json.dumps(topicGroup) 
        
    
        