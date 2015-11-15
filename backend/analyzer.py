"""Analyze a text to get localization data"""

import re
import pprint
import requests
import collections
from enum import Enum

data = requests.get('https://fr.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=1&rvprop=content&format=json&titles=Liste_des_communes_de_France_les_plus_peupl%C3%A9es').json()
content = ''.join(sorted(data['query']['pages'].items(), key=lambda x:int(x[0]))[-1][1]['revisions'][0]['*']) # seriously
section = content.split('== Communes de plus de', 1)[1].split('== Communes ayant compté plus de', 1)[0]
rows = section.split('\n|-')[1:-1]
cities = [row.split('\n| ')[2].split('[[')[1].split(']]')[0].split('|')[-1] for row in rows]
city_matcher = re.compile(r'\b{}\b'.format('|'.join(cities)))

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
