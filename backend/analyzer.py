"""Analyze a text to get localization data"""

import re
import pprint
import itertools
import collections
from enum import Enum

import collect_dataset

city_matcher = re.compile(r'\b{}\b'.format('|'.join(collect_dataset.cities)), re.I)

class ParseError(Exception):
    pass


class Transportations(Enum):
    RER = 1
    bus = 2
    metro = 3
    tramway = 4
    @staticmethod
    def from_friendly_name(name):
        return transportation_friendly_names[name.lower().strip()]
T = Transportations

transportation_friendly_names = {
        'rer': T.RER,
        'bus': T.bus,
        'métro': T.metro,
        'metro': T.metro,
        'tramway': T.tramway,
        'tram': T.tramway,
        }



line_number_pattern = re.compile(r'^([0-9]{1,3}|[a-z]{1,2})$', re.I)

Transportation = collections.namedtuple('Transportation', 'type line')

def analyze(text):
    """Tries to find localization informations from a text.

    >>> analyze('Paris re r')
    (['Paris'], [])
    >>> analyze('Paris rer foobar b')
    (['Paris'], [])
    >>> analyze('Paris rer b')
    (['Paris'], [Transportation(type=<Transportations.RER: 1>, line='B')])
    >>> analyze('Paris REr ligne B')
    (['Paris'], [Transportation(type=<Transportations.RER: 1>, line='B')])
    >>> analyze('Lyon ligne B')
    (['Lyon'], [Transportation(type=None, line='B')])
    >>> analyze('Lyon lignes B et C')
    (['Lyon'], [Transportation(type=None, line='B'), Transportation(type=None, line='C')])
    >>> analyze('Lyon lignes B, C')
    (['Lyon'], [Transportation(type=None, line='B'), Transportation(type=None, line='C')])
    >>> analyze('Lyon ligne B et C')
    (['Lyon'], [Transportation(type=None, line='B'), Transportation(type=None, line='C')])
    >>> analyze('Lyon ligne B, C')
    (['Lyon'], [Transportation(type=None, line='B'), Transportation(type=None, line='C')])
    >>> analyze('Paris ligne b bis')
    (['Paris'], [Transportation(type=None, line='B bis')])
    """
    cities = city_matcher.findall(text)
    tokens = [x.strip(',').strip(';').strip('.') for x in text.split()]
    type_ = None
    expecting_line_number = False
    transportations = []
    skip_next = False
    for (token, next_token) in zip(tokens, itertools.chain(tokens[1:], [None])):
        if skip_next:
            skip_next = False
            continue
        if token.lower() in transportation_friendly_names:
            type_ = T.from_friendly_name(token)
            expecting_line_number = True
        elif token in ('ligne', 'lignes'):
            expecting_line_number = True
        elif token in ('et', 'ou', ','):
            pass
        elif expecting_line_number and line_number_pattern.match(token):
            token = token.upper()
            if next_token and next_token.lower() == 'bis':
                token += ' bis'
                skip_next = True
            transportations.append(Transportation(type=type_, line=token))
        else:
            type_ = None
            expecting_line_number = False

    return (cities, transportations)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
