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
config.read_file(open(os.path.expanduser("/home/arnaudhub/Bureau/datalab.cnf")))

CNF = "mongo"
BDD = "Datalab"
# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
#print(client)

TBL = "MOOC_CAC"
CNF2 = "pgBDD"
pgSQLengine = create_engine("postgresql://%s:%s@%s/%s" % (config[CNF2]['user'], config[CNF2]['password'], config[CNF2]['host'], "BDD_Arnaud"))
pgSQLengine
print(pgSQLengine)

#pgSQLengine.execute("TRUNCATE \"%s\";" % TBL)
statement = text("""INSERT INTO "MOOC_test" (id, course_id, date, username, body) VALUES (:id, :cid, :date, :username,:body)""")
#statement
#~ exit()

bdd = client['Datalab'] # BDD "Datalab" de mongoDB sur serveur
#bdd
#~ print("'Datalab' Collections:")
#~ for cn in bdd.list_collection_names():
    #~ print("-"+cn)
collec = client['MOOC_GRP_CAC']['MOOC_astro']

NivMax = 0
def applat(mesg, niv):
    try:
        global NivMax
        l = len(mesg['body'])
        username = '?'
        body ='?'
        if 'username' in mesg: username = mesg['username'][:50]
        if 'body' in mesg: body = mesg['body'][:]
        pgSQLengine.execute(statement, id=mesg['id'], cid=mesg['course_id'], date=mesg['updated_at'], username=username,body=mesg['body'])
        childs = [] # liste des enfants
#        if ''
        if 'children' in mesg: childs += mesg['children']
        if 'endorsed_responses' in mesg: childs += mesg['endorsed_responses']
        if 'non_endorsed_responses' in mesg: childs += mesg['non_endorsed_responses']
        for child in childs:
    #        applat(child+l, niv+1)
            l+=applat(child,niv+1)
        #print("nombre de caractères cumulés ",l)
        if niv > NivMax:
            NivMax = niv
        print("%s %s %s : %s = %d,%d,%d" % ("  "*niv, mesg['course_id'], mesg['updated_at'], username,mesg['body'],len(mesg['body']),l))
        
    except KeyError:
        username=None
    except TypeError:
        body=None
    return l
cursor = collec.find()
for doc in cursor:
    if 'content' in doc:
        #~ pprint.pprint(doc)
        print("-------------------------------")
        longueur = applat(doc['content'], 0)
        #~ print(longueur)

print("Niv max=%d" % NivMax)