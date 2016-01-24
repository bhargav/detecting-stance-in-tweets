# import defaultdict
import IntermediateProjectWork as oldWork
from nltk.stem import *
from nltk.stem.porter import *
import numpy as np

# class item(object):
# 	def __init__(self):
# 		self.spaces = []
# 		self.isPhrase = bool()
# 		self.isWord = bool()
# 		self.initialize()
# 	def initialize(self):
# 		self.isPhrase = False
# 		self.isWord = False


# def splitWord(word, word_vec_dict):
# 	d = enchant.Dict("en_US")
# 	N = len(word)
# 	matrix = [[item() for j in range(N)] for i in range(N)]
# 	for gap in xrange(0, N):
# 		for i in xrange(0, N):
# 			j = i + gap
# 			if j >= N:
# 				break
# 			flag = False
# 			# if gap == 0:
# 			# print word[i:i+gap]
# 			if not gap:
# 				if word[i] != 'a' or word[i] != 'i':
# 					matrix[i][j].isPhrase = False
# 					matrix[i][j].isWord = False
# 				else:
# 					# print word[i]
# 					matrix[i][j].isPhrase = True
# 					matrix[i][j].isWord = True
# 					matrix[i][j].spaces.append(i)
# 					matrix[i][j].spaces.append(j)
# 			if gap and d.check(word[i:j+1]):
# 				print word[i:j+1]
# 				print i, j
# 				matrix[i][j].isPhrase = True
# 				matrix[i][j].isWord = True
# 				matrix[i][j].spaces.append(i)
# 				matrix[i][j].spaces.append(j)
# 			elif gap:
# 				for k in range (i + 1, j):
# 					if matrix[i][k].isPhrase and matrix[k+1][j].isPhrase:
# 						print i, k
# 						print k+1, j
# 						print word[i:j+1]
# 						matrix[i][j].isPhrase = True
# 						matrix[i][j].isWord = False
# 						matrix[i][j].spaces.extend(matrix[i][k].spaces)
# 						matrix[i][j].spaces.extend(matrix[k][j].spaces)
# 						matrix[i][j].spaces = list(set(matrix[i][j].spaces))
# 						break
# 	if not matrix[0][N-1].isPhrase:
# 		return word
# 	wordList = []

# 	print matrix[0][N-1].spaces
# 	for i in range(1, len(matrix[0][N-1].spaces)):
# 		wordList.append(word[matrix[0][N-1].spaces[i-1]:matrix[0][N-1].spaces[i]])
# 	print wordList
# def getStemmedTweets(taggedTweets):
# 	stemmer = PorterStemmer()
# 	for tweet in taggedTweets:
# 		print tweet['tweet']
# 		stemmedTweet = [stemmer.stem(word) for word in tweet['tweet']]
# 		print stemmedTweet

# 	return taggedTweets

def SentiWordNet(filename):
	fileReader = open(filename)
	dictionary = {}
	for line in fileReader:

		if line[0] == '#':
			continue
		splitLine = line.strip().split('\t')
		if len(splitLine) > 2:
			# print splitLine
			wordDict = {}
			wordDict['position'] = splitLine[0]
			wordDict['ID'] = splitLine[1]
			wordDict['posscore'] = splitLine[2]
			wordDict['negscore'] = splitLine[3]
			words = splitLine[4].split(' ')
			for word in words:
				dictionary[word[:len(word) - 2]] = wordDict
	return dictionary


def getTaggedTweets(filename):
	reader = open(filename)
	taggedTweets = []
	for line in reader:
		splitLine = line.strip().split('\t')
		taggedTweet = {}
		# print splitLine
		taggedTweet['tweet'] = splitLine[0].split(' ')
		taggedTweet['tags'] = splitLine[1].split(' ')
		taggedTweet['confidence'] = splitLine[2].split(' ')
		taggedTweets.append(taggedTweet)
	return taggedTweets

def readLexicon(filename):
	# nrc = './nrc_unigram.txt'
	# s140 = './s140_un'
	dictionary = {}
	reader = open(filename)
	for line in reader:
		split = line.strip().split('\t')
		# print split
		# word0 = split[0]
		# if word0[0] == '#':
		# 	word0 = word0[1:len(word0)]
		# elif word0[0] == '@':
		dictionary[split[0]] = split[1]
	return dictionary
	# print split[1]


def addTarget(taggedTweets, filename):
	reader = open(filename)
	reader.readline()
	for i in xrange(len(taggedTweets)):

		line = reader.readline()
		splitLine = line.strip().split('\t')
		# print splitLine
		taggedTweets[i]['target'] = splitLine[1]
		taggedTweets[i]['stance'] = splitLine[len(splitLine) - 1]
		# taggedTweet['stance'] = splitLine
		# print taggedTweets[i]['target']
	return taggedTweets

def getFeatures(tweets, word_vec_dict):
	X = []
	# Y = []
	# print tweets
	for tweet in tweets:
		# dummy_tweet = [tweet['target'].lower()]
		# dummy_tweet.extend(tweet['tweet'])
		# print oldWork.getSumVectors(dummy_tweet, word_vec_dict)
		x = word_vec_dict['hi']
		x = x * 0
		for word in tweet:
			x = x + oldWork.getWordVector(word, word_vec_dict)
		X.append(x)
		# if tweet['stance'] == 'AGAINST':
			# Y.append(-1)
		# elif tweet['stance'] == 'FOR':
			# Y.append(1)
		# else:
			# Y.append(0)
	# print len(X)
	# print len(tweets)
	# print X
	nrc = readLexicon('../nrc_unigram.txt')
	# print nrc
	s140 = readLexicon('../s140_unigram.txt')
	# print s140
	sumPos = 0
	sumNeg = 0
	numPos = 0
	numNeg = 0
	maxPos = -1
	maxNeg = 1
	maxPosIndex = 0
	maxNegIndex = 0
	for i in xrange(len(tweets)):
		sumPos = 0
		sumNeg = 0
		numPos = 0
		numNeg = 0
		maxPos = -1
		maxNeg = 1
		maxPosIndex = 0
		maxNegIndex = 0

		tweet = tweets[i]

		# print tweet
		for j in xrange(len(tweet)):
			word = tweet[j]
			if word in nrc:
				if nrc[word] > 0:
					numPos += 1
					if nrc[word] > maxPos:
						maxPos = nrc[word]
						maxPosIndex = j
				elif nrc[word] < 0:
					numNeg += 1
					if nrc[word] < maxNeg:
						maxNeg = nrc[word]
						maxNegIndex = j
			elif word in s140:
				if s140[word] > 0:
					numPos += 1
					if s140[word] > maxPos:
						maxPos = s140[word]
						maxPosIndex = j
				elif s140[word] < 0:
					numNeg += 1
					if s140[word] < maxNeg:
						maxNeg = s140[word]
						maxNegIndex = j
		# np.concatenate(X[i], oldWork.getWordVector(tweet[maxPosIndex], word_vec_dict))
		# np.concatenate(X[i], oldWork.getWordVector(tweet[maxNegIndex], word_vec_dict))
		# np.concatenate(X[i], numPos/len(tweet))
		# np.concatenate(X[i], numNeg/len(tweet))
		X[i] = X[i].tolist()
		# print X[i]
		# print 'index ' + str(maxPosIndex)
		# print len(tweet)
		X[i].extend(oldWork.getWordVector(tweet[maxPosIndex], word_vec_dict))
		X[i].extend(oldWork.getWordVector(tweet[maxNegIndex], word_vec_dict))
		X[i].append(numPos/len(tweet))
		X[i].append(numNeg/len(tweet))
		#print len(X[i])

        return X



	# print X
	# for index in xrange(len(taggedTweets)):


def main():
	# sentiment = SentiWordNet('./SentiWordNet_3.0.0_20130122.txt')
	taggedTweets = getTaggedTweets('../splitTaggedTweets2.txt')
	taggedTweets = addTarget(taggedTweets,'../dataset_raw/semeval2016-task6-edited-trainingdata.txt')
	writer = open('./final.txt','w')
	for tweet in taggedTweets:
		writer.write(' '.join(tweet['tweet']))
		writer.write('\t')
		writer.write(tweet['stance'])
		writer.write('\n')
	word_vec_dict = oldWork.readGloveData('../glove.twitter.27B/glove.twitter.27B.25d.txt')
	tweets = [taggedTweet['tweet'] for taggedTweet in taggedTweets]
	for i in xrange(len(tweets)):
		tweets[i] = ' '.join(tweets[i])
	getFeatures(tweets, word_vec_dict)

if __name__ == '__main__':
	main()
