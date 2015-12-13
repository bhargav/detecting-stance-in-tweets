# import defaultdict
import IntermediateProjectWork as oldWork
import enchant
from nltk.stem import *
from nltk.stem.porter import *

class item(object):
	def __init__(self):
		self.spaces = []
		self.isPhrase = bool()
		self.isWord = bool()
		self.initialize()
	def initialize(self):
		self.isPhrase = False
		self.isWord = False

def InitializeWords():
    wordlist = './wordlist' # A file containing common english words
    content = None
    with open(wordlist) as f:
        content = f.readlines()
    return [word.rstrip('\n') for word in content]


def ParseSentence(sentence, wordlist):
    new_sentence = "" # output    
    terms = sentence.split(' ')    
    for term in terms:
        if term[0] == '#': # this is hashtag, parse it
            new_sentence += ParseTag(term, wordlist)
        else: # Just append the word
            new_sentence += term
        new_sentence += " "

    return new_sentence 


def ParseTag(term, wordlist):
    words = []
    # Remove hashtag, split by dash
    tags = term[1:].split('-')
    for tag in tags:
        word = FindWord(tag, wordlist)    
        while word != None and len(tag) > 0:
            words += [word]            
            if len(tag) == len(word): # Special case for when eating rest of word
                break
            tag = tag[len(word):]
            word = FindWord(tag, wordlist)
    return " ".join(words)


def FindWord(token, wordlist):
    i = len(token) + 1
    while i > 1:
        i -= 1
        if token[:i] in wordlist:
            return token[:i]
    return None 

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

# def getStemmedTweets(taggedTweets):
# 	stemmer = PorterStemmer()
# 	for tweet in taggedTweets:
# 		print tweet['tweet']
# 		stemmedTweet = [stemmer.stem(word) for word in tweet['tweet']]
# 		print stemmedTweet

# 	return taggedTweets

def getTaggedTweets(filename):
	reader = open(filename)
	taggedTweets = []
	for line in reader:
		splitLine = line.strip().split('\t')
		taggedTweet = {}
		taggedTweet['tweet'] = splitLine[0].split(' ')
		taggedTweet['tags'] = splitLine[1].split(' ')
		taggedTweet['confidence'] = splitLine[2].split(' ')
		taggedTweets.append(taggedTweet)
	return taggedTweets

def main():
	sentiment = SentiWordNet('./SentiWordNet_3.0.0_20130122.txt')
	taggedTweets = getTaggedTweets('./tweetsTagged.txt')
	word_vec_dict = oldWork.readGloveData('./glove.twitter.27B/glove.twitter.27B.25d.txt')
	# stemmedTaggedTweets = getStemmedTweets(taggedTweets)
	wordlist = InitializeWords()
	sentence = "big #awesome-dayofmylife because #iamgreat"
	# sentence = 'oklohoma'
	splitSentence = ParseSentence(sentence, wordlist)
	print splitSentence
	# splitWord('hellohowareyou', word_vec_dict)


if __name__ == '__main__':
	main()