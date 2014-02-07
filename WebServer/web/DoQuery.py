'''
Created on Feb 6, 2014

@author: homliu
'''
from HTMLGetter import *


class DoQuery(object):

    def __init__(self):
        self.parser = LinkParser()
    
    def query(self, word):
        list = self.parser.lookup(word)
        print len(list)
        articles = []
        for l in list:
            articles.append(l.name)
        return articles
        