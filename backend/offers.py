import falcon
import json
import rethinkdb as r

class OfferListResource:
    def __init__(self):
        self._db = r.connect('localhost', 28015)

    def on_get(self, req, resp):
        """Returns all offers available"""
        cursor = r.db('voyageavecmoi').table('offers').run(self._db)
        resp.body = json.dumps(list(cursor))

app = falcon.API()
app.add_route('/api/offers', OfferListResource())
