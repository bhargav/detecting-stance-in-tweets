
class Model():

    def __init__(self, tweetID, target, tweet, stance):
        self.tweetID = tweetID
        self.target = target
        self.tweet_content = tweet
        self.stance = stance

        self.original_tweet_content = tweet
