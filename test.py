import os
from secret import CONSUMER_KEY, CONSUMER_SECRET
import twitter

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    twitter.oauth_dance("Voyage avec moi", CONSUMER_KEY, CONSUMER_SECRET,
                MY_TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

t = twitter.Twitter(auth=twitter.OAuth(
    oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

# Now work with Twitter
print(t.search.tweets(q='#VoyageAvecMoi'))
