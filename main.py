# -*- coding: utf-8 -*-
"""Copy of PyRecLabMPRec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15p2dMUzZl_keFghJtNTLdRerpZWZa0sn
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

import reclab

# download files from ml100k
#"hola"

"""
curl -L -o "u1.base" "https://drive.google.com/uc?export=download&id=1bGweNw7NbOHoJz11v6ld7ymLR8MLvBsA"
curl -L -o "u1.test" "https://drive.google.com/uc?export=download&id=1f_HwJWC_1HFzgAjKAWKwkuxgjkhkXrVg"
curl -L -o "u.item" "https://drive.google.com/uc?export=download&id=10YLhxkO2-M_flQtyo9OYV4nT9IvSESuz"
"""
#item algoritm

model = reclab.ItemKnn( dataset = 'u1.base',
                            dlmchar = b'\t',
                            header = False,
                            usercol = 0,
                            itemcol = 1,
                            ratingcol = 2 )

#tränar Item algoritm

model.train( 10, progress = False )

#för Item algoritm
recommendationList, map, ndcg = model.testrec( input_file = 'u1.test',
                                                 dlmchar = b'\t',
                                                 header = False,
                                                 usercol = 0,
                                                 itemcol = 1,
                                                 ratingcol = 2,
                                                 topn = 10,
                                                 output_file = 'ranking.json',
                                                 relevance_threshold = 2,
                                                 includeRated = False )

import numpy as np

MAP = ('MAP: %f' % ( map ) )
nDCG =( 'nDCG: %f' % ( ndcg ) )

mean_MAP_0 = float(MAP.split(':')[1])
mean_nDCG_0 = float(nDCG.split(':')[1])

#Sätter upp precision variablen (startar med 0)
precision = 0

# Läser in alla användare
users = np.loadtxt('u1.base', dtype=str, usecols=0)

# Loopar över alla användare i precision
for user_id in users:
  precisionUser = model.precision( user_id = user_id, topn = 10, relevance_threshold = 0, include_rated = False )
  
  # Sparar ner varje värde
  precision += precisionUser

# Räknar ut alla användares medelvärde genom mätvärdet/antalet användare
mean_precision_0 = precision / len(users)

# instantiate most popular recommender
model = reclab.MostPopular(dataset='u1.base',
                              dlmchar=b'\t',
                              header=False,
                              usercol=0,
                              itemcol=1,
                              ratingcol=2)

# train recommendation model
model.train( 5, progress = True )

# generate list of recommendations and metrics for users in test set
recommendList, map, ndcg = model.testrec( input_file = 'u1.test',
                                                dlmchar = b'\t',
                                                header = False,
                                                usercol = 0,
                                                itemcol = 1,
                                                ratingcol = 2,
                                                topn = 10,
                                                output_file = 'ranking.json',
                                                relevance_threshold = 2,
                                                includeRated = False )

#räknar ut avarage map och ndcg

MAP = ('MAP: %f' % ( map ) )
nDCG =( 'nDCG: %f' % ( ndcg ) )

mean_MAP_1 = float(MAP.split(':')[1])
mean_nDCG_1 = float(nDCG.split(':')[1])

#Sätter upp precision variablen (startar med 0)
precision = 0

# Läser in alla användare
users = np.loadtxt('u1.base', dtype=str, usecols=0)

# Loopar över alla användare i precision
for user_id in users:
  precisionUser = model.precision( user_id = user_id, topn = 10, relevance_threshold = 0, include_rated = False )
  
  # Sparar ner varje värde
  precision += precisionUser

# Räknar ut alla användares medelvärde genom mätvärdet/antalet användare
mean_precision_1 = precision / len(users)

# Skapar tabell över algorithmernas mätvärden
data = {
    '': ['map', 'ndcg'],
    'Most Popular': [mean_MAP_1, mean_precision_1],
    'Item KNN': [mean_MAP_0, mean_nDCG_0, mean_precision_0
}
x = pd.DataFrame(data)

#skriver ut titel och tabellen
print('Jämförelse mellan algortimerna Most Popular och User Average')
print('')
#skapar bar-chart, fixar placering av undertext och ändrar färg
ax = x.plot.bar(color=['Pink','Cyan'])

#anger positioner och etiketter för x-axeln
plt.xticks([0, 1], ['mAP', 'ndcg', 'Precision'])

# Lägger till textetiketter ovanpå varje stapel
for i, v1, v2 in zip(range(len(x)), x['Most Popular'], x['Item KNN']):
    ax.text(i-0.2, v1+0.01, str(round(v1, 4)), fontsize=10)
    ax.text(i+0.1, v2+0.01, str(round(v2, 4)), fontsize=10)

#y-label och visar graf
plt.ylabel('Medelvärdet')
plt.ylim([0, 0.35])
plt.show()