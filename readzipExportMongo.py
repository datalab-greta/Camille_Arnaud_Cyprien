"""
Created on Tue Oct  8 12:25:59 2019

@author: arnaudhub
"""

import requests, pprint, os

from pymongo import MongoClient # librairie qui va bien
import configparser

config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("/home/arnaudhub/Bureau/datalab.cnf")))

CNF = "mongo"
BDD = "Datalab"

# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
print(client)

bdd = client['Datalab'] # BDD "Datalab" de mongoDB sur serveur
bdd
    
collec = client['MOOC_GRP_CAC']['forum6']

import sys, glob, zipfile, json, ast, demjson, pprint
from demjson import decode
list = glob.glob("/home/arnaudhub/Documents/projet4/*zip")

print(list)
#~ exit()
collec.drop()
#collec.rename("FORUM")


for zip in list:
    print("-"+zip)
    zf = zipfile.ZipFile(zip, 'r') # le ZIP
#    n=0
    for zipName in zf.namelist():
#        print(zipName)
        txt = zf.read(zipName).decode("utf-8")

        # https://stackoverflow.com/questions/4162642/single-vs-double-quotes-in-json
        try:
            x = ast.literal_eval(txt)
#            pprint.pprint(x)
            flag = 'username' in x['content']
#            print(zipName+": "+x['content']['title']+", "+str(flag))
            #~ break
            collec.insert_one(x)
        except SyntaxError:
            print("erreur de lecture du fichier",zipName)

    
collec = client['MOOC_GRP_CAC']['forum6']
