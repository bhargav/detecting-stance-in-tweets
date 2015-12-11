import os
import sys
import IntermediateProjectWork as oldWork

tweetFile = './dataset_raw/semeval2016-task6-trainingdata.txt'
tweetTags = './processedTweets.txt'
tweetWriter = open(tweetTags, 'w')
tweets = oldWork.readTweets(tweetFile)
tweets = tweets[:len(tweets) - 1]
tweetClasses = tweets[len(tweets) - 1]
for tweet in tweets:
	sentence = ' '.join(tweet[1:len(tweet)])
	tweetWriter.write(sentence + '\n')
	# os.system("bash ./../ark-tweet-nlp-0.3.2/runTagger.sh " + sentence)
	# break

# print tweets[len(tweets) - 1]