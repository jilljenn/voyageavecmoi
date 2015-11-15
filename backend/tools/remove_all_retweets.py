import rethinkdb as r

if __name__ == '__main__':
    c = r.connect("localhost", 28015)

    print ('Removing the retweets.')

    r.db('voyageavecmoi').table('offers')\
        .filter(lambda offer: offer['text'].match('^RT')).delete().run(c)

    print ('All retweets are removed.')

