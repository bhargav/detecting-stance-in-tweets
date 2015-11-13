
# coding: utf-8

# In[1]:

import numpy as np


# In[2]:

dataset = []
for filename in ["./dataset_raw/semeval2016-task6-trialdata.txt", "./dataset_raw/semeval2016-task6-trainingdata.txt"]:
    f = open(filename, 'r')
    dataset  = dataset + f.readlines()

print "Number of items = ", len(dataset)


# In[3]:

glove_word_vec_file = "/Users/bhargav/Downloads/glove.twitter.27B/glove.twitter.27B.25d.txt"
print len(dataset)

def readGloveData(glove_word_vec_file):
    f = open(glove_word_vec_file, 'r')
    rawData = f.readlines()
    word_vec_dict = {}
    for line in rawData:
        line = line.strip().split()
        tag = line[0]
        vec = line[1:]
        word_vec_dict[tag] = np.array(vec, dtype=float)
            
    return word_vec_dict
            
word_vec_dict = readGloveData(glove_word_vec_file)


# In[4]:

def getWordVector(word):
    if word in word_vec_dict:
        return word_vec_dict[word]
    return np.zeros_like(word_vec_dict['hi'])
    


# In[5]:

def getSumVectors(sentence):
    numNonZero = 0
    vector = np.zeros_like(word_vec_dict['hi'])
    for word in sentence:
        vec = getWordVector(word)
        if vec.any():
            vector += vec
            numNonZero += 1
            
    if numNonZero:
        vec = vec / numNonZero
        
    return vec


# In[ ]:




# In[ ]:




# In[ ]:



