import os
import sys
import IntermediateProjectWork as oldWork


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
    	# print term
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

def main():
	wordlist = InitializeWords()
	tweetFile = '../dataset_raw/semeval2016-task6-trainingdata.txt'
	tweetTags = '../processedTweets.txt'
	tweetWriter = open(tweetTags, 'w')
	tweets = oldWork.readTweets(tweetFile)
	tweets = tweets[:len(tweets) - 1]
	tweetClasses = tweets[len(tweets) - 1]
	for tweet in tweets:
		sentence = ''
		for word in tweet:
			splitWord = word
			# print word
			if len(word) > 0 and word[0] == '#' and word != '#semst':
				splitWord = ParseSentence(splitWord, wordlist)
				# print splitWord
			sentence += splitWord
			sentence += ' '
		# sentence = ' '.join(tweet[1:len(tweet)])
		sentence = ' '.join(sentence.split())
		tweetWriter.write(sentence + '\n')
		# os.system('bash ./../ark-tweet-nlp-0.3.2/runTagger.sh '  + str(sentence))
		# print sentence
	# break

# print tweets[len(tweets) - 1]

if __name__ == "__main__":
	main()
