import falcon
import json
import rethinkdb as r

MAX_OFFERS = 100

class OfferListResource:
    def __init__(self):
        self._db = r.connect('localhost', 28015)

    def on_get(self, req, resp):
        """Returns all offers available"""
        try:
            limit, page = map(int, (req.params.get('limit', MAX_OFFERS), req.params.get('page', 1)))
        except ValueError as e:
            raise falcon.HTTPInvalidParam("Limit or page should be a number", "limit or page")

        if page < 1:
            raise falcon.HTTPInvalidParam("Page cannot be negative or null", "page")
        elif limit < 1:
            raise falcon.HTTPInvalidParam("Limit cannot be negative or null", "page")
        else:
            cursor = r.db('voyageavecmoi').table('offers').slice(page - 1).limit(limit).run(self._db)
            count = r.db('voyageavecmoi').table('offers').count()
            resp.body = json.dumps(list(cursor))
            resp.append_header('X-Max-Elements', count)

app = falcon.API()
app.add_route('/api/offers', OfferListResource())
