#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 20:06:08 2019

@author: cyprien
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 09:51:36 2019

@author: cyprien
"""
#import os.path 
#from pandas.io.json import json_normalize
#import re
#import numpy as npy
#from PIL import Image
#import collections
import pprint
import pandas as pd
import glob 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

#récupération des fichiers avec leur chemin pour le traitement itératif avec la fonction glob

path = '/home/cyprien/Documents/Projet4/fichiers_projet4/'
list_fich = glob.glob('/home/cyprien/Documents/Projet4/fichiers_projet4/*/*')

#variable dico utlisée dans la boucle
stock = dict()
#variables au format list pour extraire des chaînes de caractères de certaines valeurs pour wordcloud
pseudos = list()
body = list()

#la boucle de traitement

for fichier in list_fich:
#    print(fichier)

    it = open(fichier, 'r')
    read = it.read().strip()
    val = eval(read)
    #pprint.pprint(val)
    try:
        messages=val["content"]["body"]
    except:
        messages = ""
        
    body.append(messages)
    
    try:
        username=val["content"]["username"]    
    except:
        username=""
    pseudos.append(username)
    
    try:
        thread_type=val["content"]["thread_type"]
    except:
        thread_type=""
    
    try:
        course=val["content"]["course_id"]
    except:
        course=""
    
    try:
        forum_cat=val["content"]["courseware_title"]
    except:
        forum_cat=""
    
#replace pour garder le nom de fichier qui servira de clé unique pour le dico ainsi que d'index unique dans les dataframe    
    short = fichier.replace(path,"")
    id_cours = short.split('/')[1]
    
# création du dico 
    param = {"user":username,"type_discussion":thread_type,"nom_cours":course,"salons_forum":forum_cat}
    
    stock[id_cours] = param
    
    #print(stock)
    
#des dataframe, il fallait que ce soit des dataframe ! tableaux croisés avec classement décroissant pour les visualisations statistiques
df = pd.DataFrame.from_dict(stock, orient='index')
df2 = (pd.crosstab(df['salons_forum'],df['type_discussion'])).sort_values(by=['discussion'], ascending=False)
df3 = (pd.crosstab(df['user'],df['type_discussion'])).sort_values(by=['discussion'], ascending=False)
#Comptage simple
comptage_cours = df['nom_cours'].value_counts().head(n=20)
print(comptage_cours)

#Histogrammes
type_salon_tab = df2[:20].plot(kind = 'barh', stacked= True)
discussion_tab = df3[1:20].plot(kind='bar',stacked=True, color=['DarkBlue','LightGreen'])

#wordcloud
#extraire les pseudos et les mettre dans une chaîne de caractères, enlever les crochets et les apostrophes, tout mettre en minuscule
pseudosWCloud = str(pseudos).strip('[]').replace("'","").lower()

#mettre dans une variable les listes de mots anglais et français à filtrer, variable qui sert de paramètre pour wordcloud
stoplist = stopwords.words('french')
stoplist.extend(stopwords.words('english'))
#print(stoplist)

# wordcloud avec le filtre des mots français anglais de la variable 'stoplist'
wordcloud = WordCloud(stopwords=stoplist,max_font_size=50, max_words=100, background_color="white").generate(pseudosWCloud)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# sauvegarde de l'image générée
wordcloud.to_file("/home/cyprien/Documents/Projet4/cloud_pseudos.png")

#la même chose avec les messages
bodycloud = str(body).strip('[]').replace("'","").lower()

wordcloud = WordCloud(stopwords=stoplist,max_font_size=50, max_words=100, background_color="white").generate(bodycloud)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


wordcloud.to_file("/home/cyprien/Documents/Projet4/cloud_body.png")


