# VoyageAvecMoi

Cahier des charges : https://public.etherpad-mozilla.org/p/weYzt8Ui16

## Comment participer

### Si vous n'êtes pas développeur

Contribuez au [cahier des charges](https://public.etherpad-mozilla.org/p/weYzt8Ui16)
ou [apprenez le Python](http://apprendre-python.com) :)

### Si vous savez coder (notamment en Python)

Clonez ce repo, puis :

    cp secret_template.py secret.py

Il vous faudra enregistrer une application sur https://dev.twitter.com/apps/new.

Vous obtiendrez ainsi des identifiants CONSUMER_KEY et CONSUMER_SECRET à mettre dans votre fichier `secret.py`.

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    python test.py

Si vous obtenez un énorme JSON, c'est gagné ! Sinon, [signalez-nous](https://github.com/jilljenn/voyageavecmoi/issues) votre problème.
