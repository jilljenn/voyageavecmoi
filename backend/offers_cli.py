import pprint
import rethinkdb as r

db = r.connect('localhost', 28015)
cursor = r.db('voyageavecmoi').table('offers').run(db)
pprint.pprint(list(cursor))
