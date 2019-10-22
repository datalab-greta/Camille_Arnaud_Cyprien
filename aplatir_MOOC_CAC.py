#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:13:02 2019

@author: arnaudhub
"""

import pprint, os, pandas

from sqlalchemy import create_engine
from sqlalchemy.sql import text

from pymongo import MongoClient # librairie qui va bien
import configparser
#import psycopg2

config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("/home/ca/Documents/datalab.cnf")))

CNF = "mongo"
BDD = "Datalab"
# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
#print(client)

TBL = "MOOC_CAC"
CNF2 = "pgBDD"
pgSQLengine = create_engine("postgresql://%s:%s@%s/%s" % (config[CNF2]['user'], config[CNF2]['password'], config[CNF2]['host'], "BDD_Arnaud"))
#pgSQLengine
print(pgSQLengine)
#pgSQLengine.execute("TRUNCATE \"%s\";" % TBL)

           
statement = text("""INSERT INTO "MOOC_CAC" (id, course_id, date, username) VALUES (:id, :cid, :date, :username)""")
#statement

#~ exit()

bdd = client['Datalab'] # BDD "Datalab" de mongoDB sur serveur
#bdd
#~ print("'Datalab' Collections:")




#~ for cn in bdd.list_collection_names():
    #~ print("-"+cn)
collec = client['MOOC_GRP_CAC']['Zip']
#statement
#def applat(mesg, niv):
           
#statement = text("""INSERT INTO "mooc_astro" (id, course_id, date, username) VALUES (:id, :cid, :date, :username)""")
#statement

#~ exit()

#bdd = client['Datalab'] # BDD "Datalab" de mongoDB sur serveur
#bdd
#~ print("'Datalab' Collections:")
#~ for cn in bdd.list_collection_names():
    #~ print("-"+cn)
#collec = client['MOOC_GRP_CAC']['']
#statement
#def applat(mesg, niv):
#    try:
#        l = len(mesg['body'])
#        pgSQLengine.execute(statement, id=mesg['id'], cid=mesg['course_id'], date=mesg['updated_at'], username=mesg['username'])
#        childs = [] # liste des enfants
#        if 'children' in mesg: childs += mesg['children']
#        if 'endorsed_responses' in mesg: childs += mesg['endorsed_responses']
#        if 'non_endorsed_responses' in mesg: childs += mesg['non_endorsed_responses']
#        for child in childs:
#    #        applat(child+l, niv+1)
#            l+=applat(child,niv+1)
#        #print("nombre de caractères cumulés ",l)
##        print("%s %s %s : %s = %d,%d" % ("  "*niv, mesg['course_id'], mesg['updated_at'], mesg['username'],len(mesg['body']),l))
#        return l
#    except:
#        pass
#
#        
#cursor = collec.find()
#cursor
#for doc in cursor:
#    if 'content' in doc:
#        #~ pprint.pprint(doc)
#        print("-------------------------------")
#        longueur = applat(doc['content'], 0)
#        print(longueur)

NivMax = 0
def applat(mesg, niv):
    try:
        global NivMax
        l = len(mesg['body'])
        username = '?'
        if 'username' in mesg: username = mesg['username'][:50]
        pgSQLengine.execute(statement, id=mesg['id'], cid=mesg['course_id'], date=mesg['updated_at'], username=username)
        childs = [] # liste des enfants
        if 'children' in mesg: childs += mesg['children']
        if 'endorsed_responses' in mesg: childs += mesg['endorsed_responses']
        if 'non_endorsed_responses' in mesg: childs += mesg['non_endorsed_responses']
        for child in childs:
    #        applat(child+l, niv+1)
            l+=applat(child,niv+1)
        #print("nombre de caractères cumulés ",l)
        if niv > NivMax:
            NivMax = niv
        print("%s %s %s : %s = %d,%d" % ("  "*niv, mesg['course_id'], mesg['updated_at'], username,len(mesg['body']),l))
        
    except KeyError:
        username=None
    return l
cursor = collec.find()
for doc in cursor:
    if 'content' in doc:
        #~ pprint.pprint(doc)
        print("-------------------------------")
        longueur = applat(doc['content'], 0)
        #~ print(longueur)
        
print("Niv max=%d" % NivMax)

#    try:
#        l = len(mesg['body'])
#        pgSQLengine.execute(statement, id=mesg['id'], cid=mesg['course_id'], date=mesg['updated_at'], username=mesg['username'])
#        childs = [] # liste des enfants
#        if 'children' in mesg: childs += mesg['children']
#        if 'endorsed_responses' in mesg: childs += mesg['endorsed_responses']
#        if 'non_endorsed_responses' in mesg: childs += mesg['non_endorsed_responses']
#        for child in childs:
#    #        applat(child+l, niv+1)
#            l+=applat(child,niv+1)
#        #print("nombre de caractères cumulés ",l)
##        print("%s %s %s : %s = %d,%d" % ("  "*niv, mesg['course_id'], mesg['updated_at'], mesg['username'],len(mesg['body']),l))
#        return l
#    except:
#        pass
#
#        
#cursor = collec.find()
#cursor
#for doc in cursor:
#    if 'content' in doc:
#        #~ pprint.pprint(doc)
#        print("-------------------------------")
#        longueur = applat(doc['content'], 0)
#        print(longueur)
#
#NivMax = 0
#def applat(mesg, niv):
#    try:
#        global NivMax
#        l = len(mesg['body'])
#        username = '?'
#        if 'username' in mesg: username = mesg['username'][:50]
#        pgSQLengine.execute(statement, id=mesg['id'], cid=mesg['course_id'], date=mesg['updated_at'], username=username)
#        childs = [] # liste des enfants
#        if 'children' in mesg: childs += mesg['children']
#        if 'endorsed_responses' in mesg: childs += mesg['endorsed_responses']
#        if 'non_endorsed_responses' in mesg: childs += mesg['non_endorsed_responses']
#        for child in childs:
#    #        applat(child+l, niv+1)
#            l+=applat(child,niv+1)
#        #print("nombre de caractères cumulés ",l)
#        if niv > NivMax:
#            NivMax = niv
#        print("%s %s %s : %s = %d,%d" % ("  "*niv, mesg['course_id'], mesg['updated_at'], username,len(mesg['body']),l))
#        
#    except KeyError:
#        username=None
#        return l
#    
#cursor = collec.find()
#for doc in cursor:
#    if 'content' in doc:
#        #~ pprint.pprint(doc)
#        print("-------------------------------")
#        longueur = applat(doc['content'], 0)
#        #~ print(longueur)
#        
#print("Niv max=%d" % NivMax)

