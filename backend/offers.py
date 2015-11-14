import falcon
import json
from tinydb import TinyDB, Query

Tweets = Query()

class OfferListResource:
    def __init__(self):
        self._db = TinyDB('tweets.json')

    def on_get(self, req, resp):
        """Returns all offers available"""
        resp.body = json.dumps(self._db.search(Tweets.offer == True))

class PendingListResource:
    def __init__(self):
        self._db = TinyDB('tweets.json')

    def on_get(self, req, resp):
        """Returns all pending tweets available"""
        resp.body = json.dumps(self._db.search(Tweets.offer == False))

app = falcon.API()
app.add_route('/offers', OfferListResource())
app.add_route('/pending', PendingListResource())
