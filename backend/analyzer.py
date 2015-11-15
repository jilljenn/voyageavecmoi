"""Analyze a text to get localization data"""

import re
import os
import json
import pprint
import urllib
import requests
import collections
from enum import Enum

DATASET_DIR = 'dataset/'
CITIES_FILE = 'dataset/cities.txt'
STATIONS_FILE = 'dataset/stations.json'

class PageDoesNotExist(Exception):
    pass

redirect_pattern = re.compile('#REDIRECTION [[(?P<target>.*)]]')
def wikipedia_query(name):
    title = urllib.parse.urlencode({'titles': name.replace(' ', '_')})
    data = requests.get('https://fr.wikipedia.org/w/api.php?action=query&prop=revisions&rvlimit=1&rvprop=content&format=json&{}'.format(title)).json()
    page = sorted(data['query']['pages'].items(), key=lambda x:int(x[0]))[-1][1]
    if 'revisions' not in page:
        raise PageDoesNotExist()
    content = ''.join(page['revisions'][0]['*'])
    redirection = redirect_pattern.match(content)
    if redirection:
        return wikipedia_query(redirection.group('target'))
    return content

if not os.path.isdir(DATASET_DIR):
    os.mkdir(DATASET_DIR)

if os.path.isfile(CITIES_FILE):
    with open(CITIES_FILE) as fd:
        # Load lines and remove empty lines
        cities = list(filter(bool, fd.read().split('\n')))
else:
    print('Liste des villes non trouvée ; téléchargement.')
    content = wikipedia_query('Liste_des_communes_de_France_les_plus_peuplées')
    section = content.split('== Communes de plus de', 1)[1].split('== Communes ayant compté plus de', 1)[0]
    rows = section.split('\n|-')[1:-1]
    cities = [row.split('\n| ')[2].split('[[')[1].split(']]')[0].split('|')[-1] for row in rows]
    with open(CITIES_FILE, 'a') as fd:
        fd.write('\n'.join(cities))
        fd.write('\n')
city_matcher = re.compile(r'\b{}\b'.format('|'.join(cities)))

stations_template_pattern = re.compile(r'\{\{(?P<page>Métro de [^/]+/stations (?P<number>[A-Za-z0-9]+))\}\}')
station_link_pattern = re.compile(r'\[\[(?P<name1>[^(\]]+) \(métro de [^|\]]+\)\|(?P<name2>[^\]]+)\]\]')
if os.path.isfile(STATIONS_FILE):
    with open(STATIONS_FILE) as fd:
        stations = json.load(fd)
else:
    print('Liste des stations non trouvées ; téléchargement.')
    stations = {}
    for city in cities[0:15]: # Check only for the 15 biggest ones
        # Fetch the content of the main page
        try:
            content = wikipedia_query('Liste des stations du métro de {}'.format(city))
        except PageDoesNotExist:
            continue

        # The page is made of templates which hold the content.
        # Get the list of templates.
        templates = stations_template_pattern.finditer(content)
        city_stations = {}
        for template in templates:
            line_link = template.group('page')
            # Get all station names in that template
            content = wikipedia_query('Modèle:{}'.format(line_link))
            links = station_link_pattern.finditer(content)
            link_names = [x.group('name2').split('<')[0] for x in links]
            city_stations[template.group('number')] = link_names
        stations[city] = city_stations
    with open(STATIONS_FILE, 'a') as fd:
        json.dump(stations, fd, indent=4, sort_keys=True)


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
