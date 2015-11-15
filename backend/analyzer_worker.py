from analyzer import analyze
import rethinkdb as r

def serialize_transport(transport):
    return {
        'type': None if transport.type is None else transport.type.name,
        'line': transport.line
    }

def can_process(tweet):
    return 'text' in tweet

def update(c, id, updated_stuff):
    r.db('voyageavecmoi').table('offers').get(id).update(updated_stuff)\
        .run(c)

def classify_tweet(c, tweet):
    cities, transportations = analyze(tweet['text'])
    if len(cities) > 0 or len(transportations) > 0:
        update(c, tweet['id'], {
            'cities': cities,
            'transportations': map(serialize_transport, transportations),
            'confirmedAsOffer': True
        })
        print ('Updated a tweet.')
    else:
        print ('Ignored the update')

def process_tweets(c):
    print ('Processing new tweets.')
    feed = r.db('voyageavecmoi').table('offers')\
        .filter(r.row['confirmedAsOffer'] == False).changes().run(c)
    for change in feed:
        print (change)
        if change['new_val'] is not None and can_process(change['new_val']):
            new_tweet = change['new_val']
            classify_tweet(c, new_tweet)
        else:
            print ('Ignored change: {}'.format(change))

def classify_old_tweets(c):
    cursor = r.db('voyageavecmoi').table('offers')\
        .filter(r.row['confirmedAsOffer'] == False)\
        .run(c)

    for tweet in cursor:
        classify_tweet(c, tweet)

    print ('Classified all old tweets.')

if __name__ == '__main__':
    try:
        c = r.connect("localhost", 28015)
        print ('Analyzer connected to DB. Processing tweets until I die!')
        classify_old_tweets(c)
        process_tweets(c)
    except KeyboardInterrupt:
        print ('Analyzer exiting!')

