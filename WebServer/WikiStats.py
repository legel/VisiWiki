'''
Created on Feb 1, 2014

@author: homliu
'''

import os
from os import walk
import gzip

class LinkStat:
    def __init__(self, name, count):
        self.name = name
        self.count = count
    
    def name(self):
        return self.name
    
    def count(self):
        return self.count
    
    def __str__(self):
            return "<count:%s name:%s>" % (self.count, self.name)
    
    
class WikiStatsParser:
    def __init__(self):
        pass
        
    def setDataSource(self, path):
        self.path =  path
        self.max =0
        self.totalProcessed =0
        print self.path 
    
    def process(self):
        files = []
        linkDict = {}
        linkList = []
        if(not os.path.isfile(self.path)):
            for (dirpath, dirnames, filenames) in walk(self.path):
                for t in filenames:
                    f = dirpath+t
                    if (os.path.isfile(f)):
                        files.append(f)
        else:
            files.append(self.path)
         
        for file in files:
            print "Processing file:%s" %(file)
            try:
                self.processFile(file,linkDict,linkList )
            except:
                print "Error Processing:%s" %(file)
        return linkDict
    
    def processFile(self,path,linkDict,linkList): #Return URL + counts
        i = 0
        file =None
        if(path.endswith(".gz")):
            file = gzip.open(path)
        else:
            file = open(path)
        for line in file:
            words = line.split()
            titleLower =words[1].lower();
            if words[0].lower() != "en" or int(words[2])<50 or \
               titleLower.startswith("special:") or \
               titleLower.startswith("file:") or \
               titleLower.startswith("data:") or \
               titleLower.startswith("portal:") or \
               titleLower.startswith("category:") or \
               titleLower.startswith("help:") or \
               titleLower.startswith("wikipedia:") or\
               titleLower.find("wikimedia.org")!=-1:
                    continue
            #print line
            i +=1
            #if words[1].lower() == 'facebook':
            #    print  words[2]
            
            total = linkDict.get(words[1],0) + int( words[2])
            linkDict[words[1]] = total 
            
            if total > self.max:
                self.max = total
            
            #if words[1].lower() == 'facebook':
            #    print linkDict[words[1]]
            
            #linkList.append(LinkStat(words[1],int(words[2])))
            
        #print linkDict
        #linkList.sort(key = lambda x : x.count, reverse=True)
        
        #for node in linkList:
        #    print node
            
        print "Size:%d" % ( len(linkDict)) 
        print "Max Freq: %d" % (self.max)
        self.totalProcessed += i
        return linkDict
        #print linkList
        
        
    
class TotalStatsParser:
    def __init__(self):
        pass
        
    def setDataSource(self, path):
        self.path =  path
        
    def process(self):
        files = []
        linkDict = {}
        linkList = []
        files.append(self.path)
         
        for file in files:
            print "Processing file:%s" %(file)
            try:
                self.processFile(file,linkDict,linkList )
            except:
                print "Error Processing:%s" %(file)
        return linkDict
    
    def processFile(self,path,linkDict,linkList): #Return URL + counts
        i = 0
        file =None
        file = open(path)
            
        for line in file:
            words = line.split()
            titleLower =words[1].lower();
            #print line
            i +=1
            #if words[1].lower() == 'facebook':
            #    print  words[2]
            
            linkDict[words[0]] = int( words[1]) 
            
            
        print "Size:%d" % ( len(linkDict)) 
        return linkDict
        #print linkList
          
#Pre-processsing stats   
if __name__ == '__main__':
    obj =  WikiStatsParser()
    obj.setDataSource('./Data/')
    dict = obj.process()
    
    print "outputing..."
    f = open('./output/total_stats', 'w')
    for key, value in dict.items():
        f.write( "%s %s\n" % (key, value))
    f.close()
    print "done."
    
    