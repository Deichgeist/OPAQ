#!/bin/python3
#
# (c) 2022, 
#

import numpy  as np
import pandas as pd
import re
import requests
import time
import json
from bs4 import BeautifulSoup

baseurl = 'https://www.vffow.org/content/datenbanken/online-personenquellen/kirchenbuchquellen/quellen-nach-landkreisen-sortiert/'

Landkreise = []

# 1. Read Start-Page and collect all Landkreise:
session    = requests.Session()
req        = session.get( baseurl )
cookies    = session.cookies;
soup       = BeautifulSoup(req.content, 'html.parser')
s_select   = soup.find("select", {"name": "kreis"})
anz_kreise  = 0
anz_kirchen = 0
anz_buecher = 0

for s_option in s_select('option') :
    kreisname = s_option.string
    if not kreisname == 'Land-/Stadtkreis' :
        anz_kreise = anz_kreise +1;
        print(anz_kreise, ': ',  kreisname)
        # Go and get Website for this Kreis:
        pdata = {
            'kreis' : kreisname,
            'Absenden' : 'Daten absenden'
        }
        postreq = session.post(baseurl, data=pdata)
        if postreq.status_code == 200 :
            Landkreis = {
                'Kreisname' : kreisname,
                'Kirchspiele' : dict()
            }
            html = BeautifulSoup(postreq.content, 'html.parser')
            # Okay this html is programmed very unproffesional. We select the second occurency of fieldset
            # within this we need to alternating look for h4 tags and tables:
            # The whole code is full of bugs and unvalid tags..... let's try what we can read:
            
            # Let'S find all tbody elements. To gather the Kirchspiel we will search backwards for the corresponding p element:
            tbodies = html.find_all('tbody')
            for tb in tbodies :
                tr  = tb.find('tr')
                tds = tr('td')
                # We only use the the table rows with 10 columns:
                if len(tds) == 10:
                    #print('===============================================================================')
                    # Go backwards to find the prvious <p> element to gather Kirchspiel:
                    backp = tb.find_previous('p', {"style":"background-color: #FFFEDE;"})
                    #print(backp)
                    kirchspiel = backp.string.strip().replace('\n', ' ').replace('\r', '').replace('  ',' ')
                    #print('        Kirchspiel:', kirchspiel )
                    # Check if Kirchspiel already exists in Landkreis, otherwise add it:
                    if kirchspiel in Landkreis['Kirchspiele'] :
                        kirche = Landkreis['Kirchspiele'][kirchspiel]
                    else :
                        kirche = { 'Name': kirchspiel, 'Buecher': list() }
                        Landkreis['Kirchspiele'][kirchspiel] = kirche
                        anz_kirchen = anz_kirchen + 1
                        print('        Kirchspiel:', kirchspiel )
                    
                    gemeinde        = tds[0].get_text()
                    konfession      = tds[1].get_text()
                    taufe           = tds[2].get_text()
                    trauung         = tds[3].get_text()
                    sterbe          = tds[4].get_text()
                    sonstige        = tds[5].get_text()
                    anmerkung       = tds[6].get_text()
                    plattform       = tds[7].get_text()
                    film            = tds[8].get_text()
                    link            = tds[9].a['href']
                    # Transfer to dict:
                    buch = {
                       'Gemeinde' :  gemeinde,
                       'Konfession' : konfession,
                       'Taufen' : taufe,
                       'Trauungen' : trauung,
                       'Verstorbene' : sterbe,
                       'Sonstige' : sonstige,
                       'Anmerkung' : anmerkung,
                       'Plattform' : plattform,
                       'Film' : film,
                       'Link' : link
                    }
                    kirche['Buecher'].append(buch)
                    anz_buecher = anz_buecher +1
            Landkreise.append(Landkreis)
       
    
# Convert Data structure to json file:
with open("opaq.json", "w", encoding='utf8') as data_file:
    json.dump(Landkreise, data_file, indent=4, sort_keys=True, ensure_ascii=False)

# Print some collection stats:
print("=========================================================================")
print("Anzahl Landkreise:........", anz_kreise)
print("Anzahl Kirchspiele:.......", anz_kirchen)
print("Anzahl Bücher:............", anz_buecher)

