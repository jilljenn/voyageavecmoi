import os
from secret import CONSUMER_KEY, CONSUMER_SECRET
import twitter
from tinydb import TinyDB

def isTransportOffer(tweet):
    return '#VoyageAvecMoi' in tweet['text']

def store_tweets(db, tweets):
    for tweet in tweets['statuses']:
        if isTransportOffer(tweet):
            db.insert({'text': tweet['text'],
                       'user_id': tweet['user']['id'],
                       'offer': False})

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    twitter.oauth_dance("Voyage avec moi", CONSUMER_KEY, CONSUMER_SECRET,
                MY_TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

t = twitter.Twitter(auth=twitter.OAuth(
    oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

db = TinyDB('tweets.json')

store_tweets(db, t.search.tweets(q='#VoyageAvecMoi'))
