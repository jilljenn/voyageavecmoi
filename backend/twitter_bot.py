#!/usr/bin/env python3

import os
import time
import pprint
import twitter
import traceback
import rethinkdb as r
from secret import CONSUMER_KEY, CONSUMER_SECRET

def respond(text):
    print('Got one: %r' % text)
    # TODO
    return None

def isAddressedToMe(tweet):
    pprint.pprint(tweet)
    me = twitter.account.verify_credentials()['screen_name']
    return tweet['text'].lower().startswith('@' + me.lower())

def on_tweet(tweet):
    try:
        _on_tweet(tweet)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        traceback.print_exc()
def _on_tweet(tweet):
    if not isAddressedToMe(tweet):
        return
    response = respond(tweet['text'].split(' ', 1)[1])
    if not response:
        response = 'No response'
    prefix = '@%s ' % tweet['user']['screen_name']
    twitter.statuses.update(status=prefix + response, in_reply_to_status_id=tweet['id'])

def fetch_tweets(db, stream):
    s = stream.user(replies='all')
    next(s) # For some reason, the stream starts with a list of friends…
    for tweet in s:
        on_tweet(tweet)



MY_TWITTER_CREDS = os.path.expanduser('~/.voyageavecmoi_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    twitter.oauth_dance("Voyage avec moi", CONSUMER_KEY, CONSUMER_SECRET,
                MY_TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

auth = twitter.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET)

stream = twitter.TwitterStream(auth=auth, domain='userstream.twitter.com')
twitter = twitter.Twitter(auth=auth)
print('Logged to Twitter as @%s' % twitter.account.verify_credentials()['screen_name'])
try:
    db = r.connect('localhost', 28015)

    list_db = r.db_list().run(db)
    if 'voyageavecmoi' not in list_db:
        raise RuntimeError('Il faut créer la DB voyageavecmoi avec le script create_database.py avant de lancer ce script!')

    fetch_tweets(db, stream)
except Exception as e:
    print ('Une erreur est survenue!')
    print (e)
