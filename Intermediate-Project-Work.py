
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn import cross_validation

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

def getWordVector(word, word_vec_dict):
    if word in word_vec_dict:
        return word_vec_dict[word]
    return np.zeros_like(word_vec_dict['hi'])
    
def readTweets(fileName):
    file = open(fileName, 'r')
    raw_tweets = []
    tweets = []
    tweetClass = []
    line = file.readline()
    for line in file:
        raw_tweets.append(line.lower().strip().split('\t'))
    for tweet in raw_tweets:
        tweet2 = []
        tweet2.append(tweet[0])
        tweet2.append(tweet[1])
        tweet2.extend(tweet[2].strip().replace(',',' ').replace('.',' ').replace(':', ' ').split(' '))
        tweet2.append(tweet[3])    
        tweets.append(tweet2[1:len(tweet2) - 1])
        tweetClass.append(tweet[len(tweet) - 1])
    tweets.append(tweetClass)
    return tweets

def getTweetVectors(tweets, word_vec_dict):
    tweetVectors = []
    for tweet in tweets:
        # print tweet
        tweetVectors.append(getSumVectors(tweet, word_vec_dict))
    return tweetVectors

def getSumVectors(tweetData, word_vec_dict):
    numNonZero = 0
    vector = np.zeros_like(word_vec_dict['hi'])
    tweet = tweetData[1:]
    target = tweetData[0].split(' ')
    for word in target:
        #print word
        vec = getWordVector(word, word_vec_dict)
        vector = vector + vec
        if vec.sum() != 0:
            numNonZero += 1

    for word in tweet:
        vec = getWordVector(word, word_vec_dict)
        vector = vector + vec
        if vec.sum() != 0:
            numNonZero += 1

    if numNonZero:
        vector = vector / numNonZero

    return vector

def splitTweets(tweets):
    pass
    

def main():
    word_vec_dict = readGloveData('./glove.twitter.27B/glove.twitter.27B.25d.txt')
    tweets = readTweets('./dataset_raw/semeval2016-task6-trainingdata.txt')

    tweetVectors = getTweetVectors(tweets[0:len(tweets) - 1], word_vec_dict)
    print tweets[0]
    print getSumVectors(tweets[0], word_vec_dict)
    tweetClasses = set(tweets[-1])

    mapping = {'favor': 1, 'none': 0, 'against': 1}

    tweetClasses = np.asarray([mapping[x] for x in tweets[-1]])
    tweetData = np.asarray(tweetVectors)
    print tweetClasses.shape
    print tweetData.shape
    X = tweetData
    Y = tweetClasses
    clf = OneVsRestClassifier(LinearSVC(random_state=0))
    # X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.3, random_state=0)
    X_train = X[0:int(0.7 * len(X))]
    y_train = Y[0:int(0.7 * len(Y))]
    X_test = X[int(0.7 * len(X)) : len(X)]
    y_test = Y[int(0.7 * len(Y)) : len(Y)]
    clf.fit(X_train, y_train)
    print clf.score(X_test, y_test)

if __name__ == "__main__":
    main()