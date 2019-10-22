#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:14:32 2019

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
print("'Datalab' Collections:")


for cn in bdd.list_collection_names():
    print("-"+cn)
collec = client['MOOC_GRP_CAC']['forum2']

#~ exit()

#https://www.fun-mooc.fr/courses/OBSPM/62002/session01/discussion/forum/i4x-OBSPM-62002-course-session01/threads/596373d91c89dc530200a6ec
base = "https://www.fun-mooc.fr/courses/"
course = "OBSPM/62002/session01"
post = "596373d91c89dc530200a6ec"

response = requests.get(
    base+course+"/discussion/forum/"+post,
    params={'ajax': 1, 'resp_skip': 0, 'resp_limit': 25},
    #headers={'Accept': 'application/vnd.github.v3.text-match+json'},
    headers={
        #"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        #"Accept-Language": "en-US,en;q=0.5",
        "X-CSRFToken": "LB3UVX4u4E1iHvNQV9WgsWrAoJP3wjw9",
        "X-Requested-With": "XMLHttpRequest",
        #'Referer': 'https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f' ,
        'Cookie': 'defaultRes=900%2C0; csrftoken=LB3UVX4u4E1iHvNQV9WgsWrAoJP3wjw9; acceptCookieFun=on; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%226e32214a-3918-420b-b204-712107e22b72%22%2C%22options%22%3A%7B%22end%22%3A%222020-09-29T12%3A34%3A23.865Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; sessionid=on5tk73gw7gimjxiipar52jkafao0230; edxloggedin=true; edx-user-info="{\"username\": \"pad-awan\"\054 \"version\": 1\054 \"email\": \"arnaudhub@yahoo.fr\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/pad-awan\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"'


#defaultRes=900%2C0; csrftoken=LB3UVX4u4E1iHvNQV9WgsWrAoJP3wjw9; acceptCookieFun=on; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%226e32214a-3918-420b-b204-712107e22b72%22%2C%22options%22%3A%7B%22end%22%3A%222020-09-29T12%3A34%3A23.865Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; sessionid=on5tk73gw7gimjxiipar52jkafao0230; edxloggedin=true; edx-user-info="{\"username\": \"pad-awan\"\054 \"version\": 1\054 \"email\": \"arnaudhub@yahoo.fr\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/pad-awan\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"



    },
)

print(response.content)
pprint.pprint(response.json())
#envoyer le doc

collec.insert_one(response.json())


