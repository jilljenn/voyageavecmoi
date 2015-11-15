import re
import os
import json
import pprint
import urllib
import requests

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

section_title_pattern = re.compile(r'.*\b(?P<number>[A-Z]|[0-9]{1,2}( bis)?)\b.*')
stations_template_pattern = re.compile(r'\{\{(?P<page>Métro de [^/]+/stations (?P<number>[A-Za-z0-9]+))\}\}')
station_link_pattern = re.compile(r'\[\[(?P<name1>[^(\]]+) \(métro de [^|\]]+\)\|(?P<name2>[^\]]+)\]\]')
def get_station_links(content):
    links = station_link_pattern.finditer(content)
    return [x.group('name2').split('<')[0].split(' - ')[0] for x in links]
if os.path.isfile(STATIONS_FILE):
    with open(STATIONS_FILE) as fd:
        stations = json.load(fd)
else:
    print('Liste des stations non trouvée ; téléchargement.')
    stations = {}
    for city in cities[0:15]: # Check only for the 15 biggest ones
        # Fetch the content of the main page
        try:
            content = wikipedia_query('Liste des stations du métro de {}'.format(city))
        except PageDoesNotExist:
            continue

        sections = content.split('\n== ')[1:]
        city_stations = {}
        for section in sections:
            (title, content) = section.split(' ==\n')
            r = section_title_pattern.match(title)
            if not r:
                continue
            line = r.group('number')

            # The section may be made of a template which holds the content.
            # Get the list of templates.
            templates = list(stations_template_pattern.finditer(content))
            if templates:
                assert len(templates) == 1
                template = templates[0]
                line_link = template.group('page')
                # Get all station names in that template
                content = wikipedia_query('Modèle:{}'.format(line_link))
                link_names = get_station_links(content)
            else:
                link_names = get_station_links(content)
            print('{}: {}'.format(line, link_names))
            city_stations[line] = link_names
        stations[city] = city_stations
    with open(STATIONS_FILE, 'a') as fd:
        json.dump(stations, fd, indent=4, sort_keys=True)

