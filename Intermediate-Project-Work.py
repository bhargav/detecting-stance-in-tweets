
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

#glove_word_vec_file = ".//glove.twitter.27B/glove.twitter.27B.25d.txt"
#print len(dataset)

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
            
#word_vec_dict = readGloveData(glove_word_vec_file)


# In[4]:

def getWordVector(word, word_vec_dict):
    if word in word_vec_dict:
        return word_vec_dict[word]
    return np.zeros_like(word_vec_dict['hi'])
    


# In[5]:

def getSumVectors(sentence, word_vec_dict):
    numNonZero = 0
    vector = np.zeros_like(word_vec_dict['hi'])
    for word in sentence:
        vec = getWordVector(word, word_vec_dict)
        if vec.any():
            vector += vec
            numNonZero += 1
            
    if numNonZero:
        vec = vec / numNonZero
        
    return vec


def readTweets(fileName):
	file = open(fileName, 'r')
	raw_tweets = []
	tweets = []
	tweetClass = []
	line = file.readline()
	for line in file: 
		raw_tweets.append(line.lower().strip().replace(',',' ').split())
	for tweet in raw_tweets:
		tweets.append(tweet[1:len(tweet) - 1])
		tweetClass.append(tweet[len(tweet) - 1])
	tweets.append(tweetClass)
	return tweets

def getTweetVectors(tweets):
	tweetVectors = []
	for tweet in tweets:
		#print getSumVectors(tweet, word_vec_dict)
		print getSumVectors(tweet, word_vec_dict)
		tweetVectors.append(getSumVectors(tweet, word_vec_dict))
	return tweetVectors



word_vec_dict = readGloveData('./glove.twitter.27B/glove.twitter.27B.25d.txt')
tweets = readTweets('./dataset_raw/semeval2016-task6-trainingdata.txt')
tweetVectors = getTweetVectors(tweets[0:len(tweets) - 1])
print tweets[0]
print word_vec_dict['atheism']
print getSumVectors(tweets[1], word_vec_dict)


# In[ ]:




# In[ ]:




# In[ ]:



