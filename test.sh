#!/bin/bash
#curl -X POST -d 'kreis="Kreis Berent"' -d 'Aktion="Daten Absenden"'  -o test.html https://vffow.org/content/datenbanken/online-personenquellen/
curl -X POST -d 'kreis=Kreis+Berent&Absenden=Daten+absenden'  -o test.html https://vffow.org/content/datenbanken/online-personenquellen/
