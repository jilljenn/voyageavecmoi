import falcon
import json
import functools
import rethinkdb as r

MAX_OFFERS = 70 # Sufficiently low to answer as fast as possible

def get_offers(limit=MAX_OFFERS, page=1, show_all=False):
    q = r.db('voyageavecmoi').table('offers')

    if not show_all:
        q = q.filter({'confirmedAsOffer': True})

    q = q\
        .order_by(r.desc('created_at'))\
        .slice(page - 1)\
        .limit(limit)

    return q

def param(name, type_, default):
    """Decorator for resource methods to parse and validate an argument."""
    if type_ == 'bool':
        def parser(req):
            if name not in req.params:
                return default
            s = req.params.get[name]
            if s.lower() == 'false':
                return False
            elif s.lower() == 'true':
                return True
            else:
                raise falcon.HTTPInvalidParam(
                        "{} should be a boolean".format(name),
                        name)
    elif type_ == 'positive int':
        def parser(req):
            if name not in req.params:
                return default
            try:
                p = int(req.params[name])
            except ValueError as e:
                raise falcon.HTTPInvalidParam(
                        "{} should be a number".format(name),
                        name)
    else:
        raise ArgumentError('Unknown type: {}'.format(type_))

    def decorator(f):
        @functools.wraps(f)
        def newf(self, req, resp, *args, **kwargs):
            kwargs[name] = parser(req)
            return f(self, req, resp, *args, **kwargs)
        return newf
    return decorator

def paged(max_limit):
    """Decorator for parsing paging parameters."""
    def decorator(f):
        f = param('limit', 'positive int', max_limit)(f)
        f = param('page', 'positive int', 1)(f)
        return f
    return decorator


class OfferListResource:
    def __init__(self):
        self._db = r.connect('localhost', 28015)

    @paged(MAX_OFFERS)
    @param('show_all', 'bool', False)
    def on_get(self, req, resp, limit, page, show_all):
        """Returns all offers available"""


        cursor = get_offers(limit, page, show_all).run(self._db)
        resp.body = json.dumps(list(cursor))

class OfferListByCityResource:

    def __init__(self):
        self._db = r.connect("localhost", 28015)

    @paged(MAX_OFFERS)
    def on_get(self, req, resp, city_name, limit, page):
        """Returns all offers available"""

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
