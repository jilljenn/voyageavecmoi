import falcon
import json
import rethinkdb as r

MAX_OFFERS = 100

def get_offers(limit=MAX_OFFERS, page=1, show_all=False):
    q = r.db('voyageavecmoi').table('offers').slice(page - 1).limit(limit)\
        .order_by(r.desc('created_at'))
    if show_all:
        q = q.filter({'confirmedAsOffer': True})

    return q

def retrieve_paging_params(params, max_limit):
    try:
        limit, page = map(int, (params.get('limit', max_limit), params.get('page', 1)))
        if page < 1:
            raise falcon.HTTPInvalidParam("Page cannot be negative or null", "page")
        elif limit < 1:
            raise falcon.HTTPInvalidParam("Limit cannot be negative or null", "limit")
        else:
            return (limit, page)
    except ValueError as e:
        raise falcon.HTTPInvalidParam("Limit or page should be a number", "limit or page")

class OfferListResource:
    def __init__(self):
        self._db = r.connect('localhost', 28015)

    def on_get(self, req, resp):
        """Returns all offers available"""
        limit, page = retrieve_paging_params(req.params, MAX_OFFERS)

        try:
            show_all = bool(req.params.get('show_all', False))
        except ValueError as e:
            raise falcon.HTTPInvalidParam("show_all should be a boolean", "show_all")

        cursor = get_offers(limit, page, show_all).run(self._db)
        resp.body = json.dumps(list(cursor))

class OfferListByCityResource:

    def __init__(self):
        self._db = r.connect("localhost", 28015)

    def on_get(self, req, resp, city_name):
        """Returns all offers available"""
        limit, page = retrieve_paging_params(req.params, MAX_OFFERS)

        cursor = get_offers(limit, page)\
            .filter(lambda offer: offer['cities']\
                    .contains(lambda city: city.downcase() == city_name.lower()))\
            .run(self._db)

        resp.body = json.dumps(list(cursor))

class CitiesResource:

    def __init__(self):
        self._db = r.connect('localhost', 28015)

    def on_get(self, req, resp):
        """Returns all cities available"""
        cursor = r.db("voyageavecmoi").table("offers")\
            .filter({'confirmedAsOffer': True})\
            .concat_map(lambda offer: offer['cities'])\
            .distinct()\
            .run(self._db)

        resp.body = json.dumps(list(cursor))


app = falcon.API()
app.add_route('/api/offers', OfferListResource())
app.add_route('/api/offers/{city_name}', OfferListByCityResource())
app.add_route('/api/cities', CitiesResource())
