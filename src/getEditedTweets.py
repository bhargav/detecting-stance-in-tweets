import os
import sys
import IntermediateProjectWork as oldWork

origTweetFile = '../dataset_raw/semeval2016-task6-trainingdata.txt'

origTweets = oldWork.readTweets(origTweetFile)
origTweetClasses = origTweets[len(origTweets) - 1]
origTweets = origTweets[:len(origTweets) - 1]

origTweetReader = open(origTweetFile)

taggedTweetFile = '../tweetsTagged.txt'
taggedTweetReader = open(taggedTweetFile)

outputFile = '../dataset_raw/semeval2016-task6-edited-trainingdata.txt'
outputWriter = open(outputFile, 'w')

origLine = origTweetReader.readline()
outputWriter.write(origLine)
# print origTweets[0]
for taggedTweet in taggedTweetReader:
	print taggedTweet
	origLine = origTweetReader.readline()
	# print 'yo'
	origLineSplit = origLine.split('\t')
	# print origLineSplit
	outputWriter.write(origLineSplit[0] + '\t' + origLineSplit[1] + '\t')
	# print taggedTweet
	line = taggedTweet.strip().split('\t')
	tweetString = line[0]
	tweetList = tweetString.split(' ')
	tagsString = line[1]
	tagsList = tagsString.split(' ')
	confidenceString = line[2]
	confidenceList = confidenceString.split(' ')
	removeWords = []
	for tagIndex in xrange(len(tagsList)):
		if tagsList[tagIndex] == '#':
			removeWords.append(tweetList[tagIndex])
	for word in removeWords:
		tweetList.remove(word)
	# print tweetList
	editedTweetString = ' '.join(tweetList)
	print editedTweetString
	# print editedTweetString
	outputWriter.write(editedTweetString + '\t' + origLineSplit[3])
	# print len(tweetList)
	# print len(tagsList)
	# print len(confidenceList)
	# break
