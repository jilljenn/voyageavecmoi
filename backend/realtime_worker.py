import os
from retry.api import retry
from secret import CONSUMER_KEY, CONSUMER_SECRET
import twitter
import rethinkdb as r
import arrow

MAX_TRIES = 3 # Number of times we try to get a tweet before giving up

def isTransportOffer(tweet):
    hashtags = {x['text'] for x in tweet.get('entities', {}).get('hashtags', [])}
    return 'VoyageAvecMoi' in hashtags

def isRetweet(tweet):
    return 'retweeted_status' in tweet

def get_tweet_data(tweet):
    return {
        'text': tweet['text'],
        'id': tweet['id_str'],
        'user': {
            'id': tweet['user']['id_str'],
            'name': tweet['user']['name'],
            'screen_name': tweet['user']['screen_name']
        },
        'created_at': arrow.get(tweet['created_at'], 'MMM DD HH:mm:ss Z YYYY').to('utc').timestamp,
        'confirmedAsOffer': False
    }

class Logger:
    def warning(self, fmt, error, delay):
        print('Error: %r' % error)
        print('Retrying in %s seconds.' % delay)

@retry(delay=5, logger=Logger())
def fetch_tweets(db, stream):
    for tweet in stream.statuses.filter(track='#VoyageAvecMoi'):
        print ('Got tweet.')
        if isRetweet(tweet):
            print('Is a retweet.')
        elif not isTransportOffer(tweet):
            print('Not a transport offer.')
        else:
            print ('Adding tweet from @{}'.format(tweet['user']['screen_name']))
            tweet_data = get_tweet_data(tweet)
            r.db('voyageavecmoi').table('offers').insert(tweet_data).run(db)
            print('Done.')

MY_TWITTER_CREDS = os.path.expanduser('~/.voyageavecmoi_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    twitter.oauth_dance("Voyage avec moi", CONSUMER_KEY, CONSUMER_SECRET,
                MY_TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

auth = twitter.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET)

stream = twitter.TwitterStream(auth=auth)
try:
    db = r.connect('localhost', 28015)

    list_db = r.db_list().run(db)
    if 'voyageavecmoi' not in list_db:
        raise RuntimeError('Il faut créer la DB voyageavecmoi avec le script create_database.py avant de lancer ce script!')

    fetch_tweets(db, stream)
except Exception as e:
    print ('Une erreur est survenue!')
    print (e)
