
""" Twitter Section """

import twitter
import json
from itertools import chain
import numpy as np

import TextMiner
from TextMiner import clean_string
from textblob import TextBlob

from Keys import environment_vars

class TwitterApi:
    def __init__(self, q, count=200):

        ## Class-wide vars:

        self.q = q
        self.site = site
        self.count = count

        # Authorizations are sorted below, consider using environment vars!!!

        self.CONSUMER_KEY = environment_vars("keys.env")["TWITTER_CONS"]
        self.CONSUMER_SECRET = environment_vars("keys.env")["TWITTER_CONS_SECRET"]
        # to get the oauth credential you need to click on the 'Generate access token' button:
        self.OAUTH_TOKEN = environment_vars("keys.env")["TWITTER_OAUTH"]
        self.OAUTH_TOKEN_SECRET = environment_vars("keys.env")["TWITTER_OAUTH_SECRET"]
        self.auth = twitter.oauth.OAuth(self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET,
                                        self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.twitter_api = twitter.Twitter(auth=self.auth)


    def apiParser(self):

        self.search_results = self.twitter_api.search.tweets(q=self.q, count=self.count)  # search for your query 'q' x times
        self.statuses = self.search_results['statuses']  # extract the tweets found
        # print(type(self.statuses))
        # print(json.dumps(self.statuses[0], indent=1))

        return self.statuses


    def userRetriever(self):

        self.status_texts = [status['text'] for status in self.apiParser()]

        # Compute a collection of all words from all tweets

        self.words = [w for t in self.status_texts for w in t.split()]  # split the string on the empty spaces

        # words = [clean_string(i) for i in status_texts]

        self.final = [clean_string(i) for i in self.words]

        # Explore the first 5 items for each...

        print(json.dumps(self.status_texts[0:5], indent=1))
        print(json.dumps(self.words[0:5], indent=1))

        return list(chain.from_iterable(self.final))




"""
Naive cutoff used below is only temporary
"""

def sentiment(site, ntweet, result):  # Simple method to return naive print output:
    if result < 0:
        return f"Over the last {ntweet} tweets, {site} received an average negative sentiment"
    elif  result >= 0 and result <= 0.4:
        return f"Over the last {ntweet} tweets, {site} received an average neutral sentiment"
    else:
        return f"Over the last {ntweet} tweets, {site} received an overwhelmingly positive sentiment"

# Main Program:

site = input('Which stonk would you like to get info about?')
t = TwitterApi(q=site)
t.apiParser()

twitter_out = {"Word": t.userRetriever(),
 "Score": [TextBlob(i).sentiment.polarity for i in t.userRetriever()]}

print("Output: ")
print(sentiment(site, 200, np.mean(twitter_out["Score"])))