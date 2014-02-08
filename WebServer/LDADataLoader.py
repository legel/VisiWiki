'''
Created on Feb 8, 2014

@author: homliu
'''
from web.MySQLConnector import *

mysql = MySQLConnector()


if __name__ == '__main__':
    file = open('./Data/LDAParsedOutputFile.txt')
    i = 0
    for line in file:
        words=line.split('#')
        article_id = int(words[0])
        topic_id =  int( words[1])
        weight =  float(words[2])
        article_list_str = words[3][1:len(words[3])-2]
        article_list = [ int(b) for b in article_list_str.split(',') ]
        mysql.insertLDAMapping(article_id, topic_id, weight, article_list)
        if(i%1000 ==0):
            print i
        i+=1
    
    
    