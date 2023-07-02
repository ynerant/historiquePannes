#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auteurs: Romain MAZIERE and Gaspard FEREY (Arcep)
#
# Processus de récupération des sites indisponibles de France métropolitaine
# publiés par les opérateurs et sauvegarde des données uniformisées
# aux formats CSV, JSON et GeoJSON.
# 
# Nécessite Python 3.7

# Liste des opérateurs avec les urls de téléchargement des fichiers, les formats ainsi que la correspondance des colonnes
operateurs = [
  {
    'name': 'Free',
    'code': 'free',
    'url' : 'https://mobile.free.fr/account/antennes-relais-indisponibles.csv',
    'type': 'csv',
    'separator' : ';',
    'skipheader': 0,
    'skipfooter': 0,
    'structure' : { # Table de renommage des champs pour harmonisation entre opérateurs
      "fin_prev": 'fin',
    },
    'reformatting': {}
  },
  {
    'name': 'Orange',
    'code': 'orange',
    'url' : 'https://couverture-mobile.orange.fr/mapV3/siteshs/data/Liste_des_antennes_provisoirement_hors_service.csv',
    # 'encoding':'windows-1250',
    'type': 'csv',
    'separator' : ';',
    'skipheader': 0,
    'skipfooter': 0,
    'structure' : {
      "op_leader"              : 'propre',
      "debut_interruption_voix": 'debut_voix',
      "fin_interruption_voix"  : 'fin_voix',
      "debut_interruption_data": 'debut_data',
      "fin_interruption_data"  : 'fin_data'
    },
    # Table de reformattage des champs (typiquement les dates).
    # 'match'  désigne un motif (expression régulière) utilisé pour filtrer le champs fourni par l'opérateur
    # 'format' désigne le nouveau format à appliquer au filtrage trouvé
    'reformatting': {
        'debut_voix': {'match': '([0-9]{2})/([0-9]{2})/([0-9]{4}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', 'format': '{2}-{1}-{0} {3}:{4}:{5}'},
        'debut_data': {'match': '([0-9]{2})/([0-9]{2})/([0-9]{4}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', 'format': '{2}-{1}-{0} {3}:{4}:{5}'},
        'fin_voix'  : {'match': '([0-9]{2})/([0-9]{2})/([0-9]{4})', 'format': '{2}-{1}-{0}'},
        'fin_data'  : {'match': '([0-9]{2})/([0-9]{2})/([0-9]{4})', 'format': '{2}-{1}-{0}'},
    }
  },
  {
    'name': 'SFR',
    'code': 'sfr',
    'url' : 'https://static.s-sfr.fr/media/export-arcep/siteshorsservices.csv',
    'type': 'csv',
    'separator' : ';',
    'skipheader': 3,
    'skipfooter': 12,
    'structure' : {
      "Lat"                         : 'lat',
      "Lon"                         : 'lon',
      "Antenne relais gérée par SFR": 'propre',
    },
    'reformatting': {}
  },
  {
    'name': 'Bouygues Telecom',
    'code': 'bytel',
    'url' : 'http://antennesindisponibles.bouyguestelecom.fr/antennesindisponibles.xls',
    'type': 'xls',
    'excelsheet' : 0,
    'excelheader': 0,
    'skipheader' : 0,
    'skipfooter' : 1,
    'structure'  : {
      "Code SI"    : 'code_site_op',
      "Région"     : 'region',
      "Département": 'departement',
      "Commune"    : 'commune',
      "Code INSEE" : 'code_insee',
      "Lat"        : 'lat',
      "Lon"        : 'lon',
      "détail"     : 'detail',
      "début"      : 'debut',
    },
    'reformatting': {}
  }
]

# Les noms des champs récupérés
status_columns       = ['2Gvoix', '3Gvoix', '3Gdata', '4Gdata', '5Gdata', 'voix', 'data']
equipment_columns    = status_columns + ['code_site_op', 'propre', 'raison', 'detail']
detail_duree_columns = ['debut_voix', 'fin_voix', 'debut_data', 'fin_data', 'debut', 'fin']
indispo_columns      = ['region', 'departement', 'code_insee', 'commune', 'lat', 'lon']
all_columns          = ['datetime', 'operateur', 'op_code'] + indispo_columns + equipment_columns + detail_duree_columns
