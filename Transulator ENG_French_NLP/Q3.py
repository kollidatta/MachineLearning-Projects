# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:24:50 2019
Submitted by : Sridatta kolli
            500888855
Link to parallel corpus :https://machinelearningmastery.com/prepare-french-english-dataset-machine-translation/

@author: prabhakar reddy
"""

import pandas as pd
import string
import numpy as np
import re
import csv
from pickle import dump
from unicodedata import normalize
import scipy.io as sio
import tensorflow as tf
from tensorflow import keras


def clean_Text(cText):
    
    
    cleaned_Text = list()
	# prepare regex for char filtering
    re_print = re.compile('[^%s]' % re.escape(string.printable))
	# prepare translation table for removing punctuationt
    table = str.maketrans('', '', string.punctuation)
    
    for line in cText:
		# normalize unicode characters
        line = normalize('NFD', line).encode('ascii', 'ignore')
        line = line.decode('UTF-8')
		# tokenize on white spacel
        line = line.split()
        # convert to lower case
        line = [word.lower() for word in line]
		# remove punctuation from each token
        line = [word.translate(table) for word in line]
		# remove non-printable chars form each token
        line = [re_print.sub('', w) for w in line]
		# remove tokens with numbers in them
        line = [word for word in line if word.isalpha()]
		# store as string
        cleaned_Text.append(' '.join(line))
        
    return cleaned_Text

def data_select(Text_fr,Text_en):
    #df_t = pd.DataFrame({'tCol':Text})
    fr_results = []
    en_results = []
    words_size = 6
    for index in range(0,len(Text_en)):
        if len(Text_en[index].split())==words_size:
            
            fr_results.append(Text_fr[index])
            en_results.append(Text_en[index])
            
    return fr_results,en_results
            
        
           
def Emat(file):
    
    results = list()
    with open(file,'r') as f:
        for line in f:
            for word in line.split():
                results.append(word) 
                
    unique_words = set(results)
    results = sorted(results)
    ranking = [results.index(v) for v in unique_words]
    return dict(zip(results, ranking))
    
   



fileName_Fr= "europarl-v7.fr-en.fr"
fileName_En="europarl-v7.fr-en.en"
#Text_fr,Text_en = load_File(fileName_Fr,fileName_En)

file_fr = open(fileName_Fr, mode = 'rt', encoding = 'utf-8')
file_en = open(fileName_En, mode = 'rt', encoding = 'utf-8')

Text_fr = file_fr.read()
file_fr.close()
Text_en = file_en.read()
file_en.close()
Text_fr = Text_fr.strip().split('\n') #doc into sentences
Text_en = Text_en.strip().split('\n')

#text cleaning
Text_fr = clean_Text(Text_fr)
Text_en = clean_Text(Text_en)

##Sentence Selection for 6 words in entire text
fr, en = data_select(Text_fr,Text_en)
#selecting 6000 
df_en = pd.DataFrame({'col':en})
df_en_6000 = df_en.head(6000)
np.savetxt(r'Emat_en.txt', df_en_6000, fmt = '%s')

df_fr = pd.DataFrame({'col':fr})
df_fr_6000 = df_fr.head(6000)
np.savetxt(r'Emat_fr.txt', df_fr_6000, fmt = '%s')

#ranking 
ranking_en = Emat('Emat_en.txt')
ranking_fr = Emat('Emat_fr.txt')

Emat_en = []
Emat_fr = []
Soe_en = [] 
Soe_fr = [] 

for i in range(0, len(en)):
    en_vec = []
    for word in en[i].split():
        en_vec.append(ranking_en[word])
    Emat_en.append(en_vec)
    soe = 0
    for word in fr[i].split():
        soe = soe + ranking_fr[word]
    Soe_fr.append(soe)
    
with open('Emat_en.csv', mode='w', newline='') as out:
    csvwrite = csv.writer(out)
    for row in Emat_en:
        csvwrite.writerow(row)

with open('Soe_fr.csv', mode='w', newline='') as out:
    csvwrite = csv.writer(out, delimiter=',')
    for row in Soe_fr:
        csvwrite.writerow([row])

df_final = pd.DataFrame({'col':Emat_en})

sio.savemat('q3.mat', {'struct':df_final.to_dict("list")}, oned_as = 'column') 

df2 = pd.DataFrame({'col':Soe_fr})
sio.savemat('q3_soe.mat', {'struct':df_final.to_dict("list")}, oned_as = 'column') 



#c_Text  = clean_Text(Text)
#data_Frame(c_Text)
#file = data_Frame_translated(c_Text)
#Emat(file)
