"""Analyze a text to get localization data"""

import re
import pprint
import itertools
import collections
from enum import Enum

import collect_dataset



line_number_pattern = re.compile(r'^([0-9]{1,3}|[a-z]{1,2})$', re.I)

################################################
# Data structures

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

Transportation = collections.namedtuple('Transportation', 'type line')



################################################
# Normalization

class shortcuts:
    """namespace"""
    remove = lambda L, x: list(filter(lambda i:i not in x, L))
    replace = lambda L, x, y: [y if i == x else i for i in L]
    remove_after = lambda L, x: list(itertools.takewhile(lambda i:i not in x, L))

class MultipleReplacer:
    """Return a callable that replaces all dict keys by the associated
    value. More efficient than multiple .replace()."""
    # From https://github.com/ProgVal/Limnoria/blob/master-2015-10-10/src/utils/str.py#L130-L142

    def __init__(self, dict_):
        self._dict = dict_
        dict_ = dict([(re.escape(key), val) for key,val in dict_.items()])
        self._matcher = re.compile('|'.join(dict_.keys()))
    def __call__(self, s):
        return self._matcher.sub(lambda m: self._dict[m.group(0)], s)
accent_replacer = MultipleReplacer({'é': 'e', 'è': 'e', 'ê': 'e', 'à': 'a', 'ù': 'u',
    '—': '-', '–': '-', '’': ' '})

def normalize_saint(name):
    """
    >>> normalize_saint(['saint', 'philibert'])
    [['philibert'], ['st', 'philibert']]
    >>> normalize_saint(['st', 'philibert'])
    [['philibert'], ['st', 'philibert']]
    """
    if 'saint' in name or 'st' in name:
        return [shortcuts.remove(name, {'saint', 'st'}),
                shortcuts.replace(name, 'saint', 'st')]
    else:
        return [name]
def normalize_conjunction(name):
    """
    >>> normalize_conjunction(['ens', 'de', 'lyon'])
    [['ens'], ['ens', 'lyon'], ['ens', 'de', 'lyon']]
    >>> normalize_conjunction(['pont', 'de', 'levallois'])
    [['levallois'], ['pont', 'levallois'], ['pont', 'de', 'levallois']]
    >>> normalize_conjunction(['porte', 'des', 'lilas'])
    [['lilas'], ['porte', 'lilas'], ['porte', 'des', 'lilas']]
    >>> normalize_conjunction(['port', 'de', 'lille'])
    [['port'], ['port', 'lille'], ['port', 'de', 'lille']]
    >>> normalize_conjunction(['les', 'agnettes'])
    [['agnettes']]
    >>> normalize_conjunction(['mairie', 'd', 'issy'])
    [['mairie'], ['mairie', 'issy'], ['mairie', 'd', 'issy']]
    """
    common_prefixes = {
            'pont', 'rue', 'avenue', 'place', 'port', 'porte',
            }
    if name[0] in {'les', 'la', 'le'}:
        return normalize_conjunction(name[1:])
    elif name == ['charles', 'de', 'gaulle']:
        return [['de', 'gaulle'], ['charles', 'de', 'gaulle']]
    elif len(name) > 2 and name[0] in common_prefixes and name[1] in ('de', 'd', 'des'):
        L = [name[2:], [name[0]] + name[2:], name]
        if len(name) == 3 and name[-1] in map(str.lower, collect_dataset.cities):
            L[0] = [name[0]]
        return L
    elif 'de' in name or 'd' in name:
        return [shortcuts.remove_after(name, ('de', 'd', 'des')),
                shortcuts.remove(name, ('de', 'd', 'des')),
                name]
    else:
        return [name]

def normalize(name):
    """Normalizes a station name so we can more easily match them with
    the database.
    Returns a list, which contains different possible normalizations, with
    different accuracies (first more prone to false positives).

    >>> normalize('Bourg   ')
    ['bourg']
    >>> normalize('Saint-Philibert')
    ['philibert', 'st philibert']
    >>> normalize('Pont de Levallois')
    ['levallois', 'pont levallois', 'pont de levallois']
    >>> normalize('Porte des Lilas')
    ['lilas', 'porte lilas', 'porte des lilas']
    >>> normalize('ENS de Lyon')
    ['ens', 'ens lyon', 'ens de lyon']
    >>> normalize('Père Lachaise')
    ['pere lachaise']
    >>> normalize("Mairie d\\'Issy")
    ['mairie', 'mairie issy', 'mairie d issy']
    >>> normalize('Mairie d’Issy')
    ['mairie', 'mairie issy', 'mairie d issy']
    """
    name = accent_replacer(name.lower()).replace('-', ' ').split()
    name = list(itertools.chain.from_iterable(x.split('\'') for x in name))
    if not name:
        return []
    names = [name]
    for pred in (normalize_saint, normalize_conjunction):
        names = itertools.chain.from_iterable(map(pred, names))
    return [' '.join(n) for n in names]


##################################################
# Find line a city from station_name

station_to_line = {}

for (city, lines) in collect_dataset.stations.items():
    for (lineno, stations) in lines.items():
        for station in stations:
            station_normalizations = normalize(station)
            for station_normalization in station_normalizations:
                if station_normalization not in station_to_line:
                    station_to_line[station_normalization] = []
                station_to_line[station_normalization].append((city, lineno))

def guess_line_from_station(station):
    """
    >>> guess_line_from_station("Agnettes")
    [('Paris', '13')]
    """
    for normalization in reversed(normalize(station)):
        # Find the closest one that matched
        if normalization in station_to_line:
            return station_to_line[normalization]

MAX_STATION_LENGTH = max(x.count(' ') for x in station_to_line)

def capture_station(tokens, right):
    """
    >>> capture_station(['foo', 'les', 'agnettes'], False)
    >>> capture_station(['foo', 'les', 'agnettes'], True)
    [('Paris', '13')]
    >>> capture_station(['les', 'agnettes', 'foo'], True)
    >>> capture_station(['les', 'agnettes', 'foo'], False)
    [('Paris', '13')]
    """
    for length in range(MAX_STATION_LENGTH, 0, -1):
        if right:
            L = tokens[-length:]
        else:
            L = tokens[0:length]
        results = guess_line_from_station(' '.join(L))
        if results:
            return results

def get_line_hints(tokens):
    """
    >>> get_line_hints(['foo', 'Belleville', 'à', 'Châtelet', 'bar'])
    [('Paris', '11')]
    >>> get_line_hints(['foo', 'St', 'Fargeau', 'à', 'Porte', 'des', 'Lilas', 'bar'])
    [('Paris', '3 bis')]
    >>> get_line_hints(['foo', 'St', 'Fargeau', 'à', 'Lilas', 'bar'])
    [('Paris', '3 bis')]
    """
    line_hints = []
    for (i, token) in enumerate(tokens):
        if token in {'-', '->', '=>', 'vers', 'à', 'a'}:
            from_station = capture_station(tokens[max(0, i-MAX_STATION_LENGTH):i], True)
            to_station = capture_station(tokens[i+1:i+MAX_STATION_LENGTH+1], False)
            if not from_station or not to_station:
                continue
            from_station = set(from_station)
            to_station = set(to_station)
            line_hints.extend(from_station & to_station)
    return line_hints


##################################################
# Analyzer

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
    >>> analyze('RER, ligne b')
    ([], [Transportation(type=<Transportations.RER: 1>, line='B')])
    """
    tokens = [x.strip(',').strip(';').strip('.') for x in text.split()]
    cities_set = set(map(str.lower, collect_dataset.cities))
    cities = [token for token in tokens if token.lower() in cities_set]
    type_ = None
    expecting_line_number = False
    transportations = []
    skip_next = 0
    for (i, token) in enumerate(tokens):
        if skip_next:
            skip_next -= 1
            continue
        if token.lower() in transportation_friendly_names:
            # This is a type of transportation
            type_ = T.from_friendly_name(token)
            expecting_line_number = True
        elif token in ('ligne', 'lignes'):
            # Doesn't do anything if there was a transportation type just
            # before, but may be used to declare a transportation
            expecting_line_number = True
        elif token in ('et', 'ou', ','):
            # in a list, just ignore it
            pass
        elif expecting_line_number and line_number_pattern.match(token):
            # This looks like a line number, and we are expecting a line
            # number
            token = token.upper()
            if i < len(tokens)-1 and tokens[-1].lower() == 'bis':
                token += ' bis'
                skip_next = 1
            transportations.append(Transportation(type=type_, line=token))
        else:
            # Just words. Reset the state.
            type_ = None
            expecting_line_number = False

    return (cities, transportations)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
