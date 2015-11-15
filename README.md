# [VoyageAvecMoi](http://www.voyageavecmoi.xyz)

Codons ensemble une application pour faciliter le traitement des tweets #VoyageAvecMoi, par exemple :

- Reconnaissance d'une ville ou d'un trajet RER
- Inscription à des alertes (ou couplage offre-demande)
- Éventuellement, établir une spécification que Twitter pourrait implémenter !

Cette liste n'est pas exhaustive, vous pouvez contribuer au cahier des charges ([accéder au pad](https://public.etherpad-mozilla.org/p/weYzt8Ui16)) !

(C'est également l'occasion de comprendre comment diable fonctionne OAuth.)

## Comment participer

### Si vous n'êtes pas développeur

Contribuez au [cahier des charges](https://public.etherpad-mozilla.org/p/weYzt8Ui16)
ou [apprenez le Python](http://apprendre-python.com) :)

### Si vous savez coder (notamment en Python ou JavaScript).

Lisez plus bas!

## Contributeurs

Clonez ce repo pour commencer.
Puis appliquez les instructions de la partie qui vous intéresse.
N'oubliez pas de vous déplacer dans le repértoire de la *bonne* partie (backend/frontend).

### Backend (Python 3.5+)

#### Mise en route
Tout d'abord, faites :

    cp secret_template.py secret.py

Il vous faudra enregistrer une application sur https://dev.twitter.com/apps/new.

Vous obtiendrez ainsi des identifiants CONSUMER_KEY et CONSUMER_SECRET à mettre dans votre fichier `secret.py`.

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    python test.py

Si vous obtenez un énorme JSON, c'est gagné ! Sinon, [signalez-nous](https://github.com/jilljenn/voyageavecmoi/issues) votre problème.

#### API
Ce projet se compose d'une API REST supporté par [Falcon](http://falconframework.org) qui va récupérer des données d'une base de donnée [RethinkDB](https://rethinkdb.com).
On a besoin d'aide pour créer plus d'endpoints et de rendre le code plus intéressant.

*Technologies:* Python 3.5, Falcon (REST API), RethinkDB.

#### Real-Time worker
Il existe un worker qui va se connecter à Twitter à l'aide de l'API Streaming (public) et appeler `filter(track='#VoyageAvecMoi')`.
Dès qu'il reçoit un nouveau tweet _contenant_ le hashtag #VoyageAvecMoi, il l'ajoute dans la DB.

Des améliorations sont possibles au niveau architectural du code (c'est du quick'n'dirty!), de plus, ça serait cool de pouvoir ajouter plus de méta-données dans le but d'apporter un meilleur service de couplage, et compagnie.

*Technologies*: Python 3.5, Twitter API, RethinkDB.

### Frontend (JavaScript ES7 - React.js)

#### Mise en route
*On présuppose que vous avez déjà un environnement Node.js v4.0.0+, si non, vous devriez jeter un coup d'oeil à [nvm](https://github.com/creationix/nvm)*
Tout d'abord, faites :

```console
npm install
```

Vous avez maintenant toutes les dépendances nécessaires.
Il suffit de `npm start` pour démarrer le serveur de développement Webpack.

#### Quelques informations à propos de l'architecture
Nous utilisons [Redux](https://github.com/rackt/redux) pour gérer l'état et [Axios](https://github.com/mzabriskie/axios) pour faire des requêtes AJAX.
Enfin, la vue est merveilleusement affiché grâce à [React](https://facebook.github.io/react/).

On a besoin d'aide sur le design, l'UX de l'application ainsi que des nombreuses choses.

#### À faire

#### Backend
Il serait absolument génial d'ajouter 2 élements:

	* Un bot capable de répondre et d'intéragir avec les personnes sur Twitter. (Il y a déjà un squelette dans `backend/twitter_bot.py`.)
	* Une API real-time avec des WebSockets ou WAMP.ws !

#### Frontend
Cela vient dans la continuité des choses à faire mais:

	* Utiliser l'API real-time pour afficher des données encore plus rapidement!
