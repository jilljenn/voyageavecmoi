"""Analyze a text to get localization data"""

import re
import pprint
import urllib
import collections
from enum import Enum

import rethinkdb as r

import collect_dataset

city_matcher = re.compile(r'\b{}\b'.format('|'.join(collect_dataset.cities)))


class Transportations(Enum):
    RER = 1
    bus = 2
    metro = 3
    tramway = 4
    @staticmethod
    def from_friendly_name(name):
        return transportation_friendly_names[name.lower()]
T = Transportations

transportation_friendly_names = {
        'rer': T.RER,
        'bus': T.bus,
        'métro': T.metro,
        'metro': T.metro,
        'tramway': T.tramway,
        'tram': T.tramway,
        'ligne': None,
        }

line_template = '(\s*(ligne)?\s*(?P<line>[0-9]{0,3}[a-z]{0,2}))'

transportation_regexp = r'\b(?P<type>{}){}\b'.format(
        '|'.join(transportation_friendly_names),
        line_template)

transportation_matcher = re.compile(transportation_regexp, re.I)

Transportation = collections.namedtuple('Transportation', 'type line')

def analyze(text):
    """Tries to find localization informations from a text.

    >>> analyze('Paris re r')
    (['Paris'], [])
    >>> analyze('Paris rer foobar b')
    (['Paris'], [Transportation(type=<Transportations.RER: 1>, line='')])
    >>> analyze('Paris rer b')
    (['Paris'], [Transportation(type=<Transportations.RER: 1>, line='B')])
    >>> analyze('Paris REr ligne B')
    (['Paris'], [Transportation(type=<Transportations.RER: 1>, line='B')])
    >>> analyze('Lyon ligne B')
    (['Lyon'], [Transportation(type=None, line='B')])
    """
    cities = city_matcher.findall(text)
    transportations = transportation_matcher.finditer(text)
    transportations = [Transportation(type=T.from_friendly_name(x.group('type')),
                                      line=x.group('line').upper())
                       for x in transportations]
    return (cities, transportations)

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

if __name__ == "__main__":
    try:
        c = r.connect("localhost", 28015)
        print ('Analyzer connected to DB. Processing tweets until I die!')
        classify_old_tweets(c)
        process_tweets(c)
    except KeyboardInterrupt:
        print ('Analyzer exiting!')

