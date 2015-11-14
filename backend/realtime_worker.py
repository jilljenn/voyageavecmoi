import os
from retry.api import retry
from secret import CONSUMER_KEY, CONSUMER_SECRET
import twitter
import rethinkdb as r

MAX_TRIES = 3 # Number of times we try to get a tweet before giving up

def isTransportOffer(tweet):
    return '#VoyageAvecMoi' in tweet['text']

def get_tweet_data(tweet):
    return {
        'text': tweet['text'],
        'id': tweet['id_str'],
        'user': {
            'id': tweet['user']['id_str'],
            'name': tweet['user']['name'],
            'screen_name': tweet['user']['screen_name']
        },
        'confirmedAsOffer': False
    }

@retry(delay=1, backoff=2)
def fetch_tweets(db, stream):
    for tweet in stream.statuses.filter(track='#VoyageAvecMoi'):
        print ('Got tweet.')
        if isTransportOffer(tweet):
            print ('Adding tweet from @{}'.format(tweet['user']['screen_name']))
            tweet_data = get_tweet_data(tweet)
            r.db('voyageavecmoi').table('offers').insert(tweet_data).run(db)

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    twitter.oauth_dance("Voyage avec moi", CONSUMER_KEY, CONSUMER_SECRET,
                MY_TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

auth = twitter.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET)

stream = twitter.TwitterStream(auth=auth)
db = r.connect('localhost', 28015)

fetch_tweets(db, stream)
