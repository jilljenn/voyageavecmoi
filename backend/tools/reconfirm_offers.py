import rethinkdb as r

def isFalseOffer(offer):
    if offer['confirmedAsOffer'] == True:
        return offer['cities'].count() == 0 and offer['transportations'].count() == 0
    else:
        return False

if __name__ == '__main__':
    c = r.connect("localhost", 28015)
    print ('Fixing all false offers (cities [] == 0 and transportations [] == 0)')
    r.db('voyageavecmoi').table('offers')\
        .filter(isFalseOffer)\
        .update({'confirmedAsOffer': False})\
        .run(c)
    print ('Fixed false offers.')
