from datetime import datetime, timedelta
from flask import Flask, render_template, request
import requests
import deepl
import os

# import des clés api nécesaires au fonctionnement du projet

#nasa_api_key = os.environ['NASA_API_KEY']
nasa_api_key = "aG0heyBXpIMVchlDs1dktmwELh91BZZeawAADWzb"
#deepl_api_key = os.environ['DEEPL_API_KEY']
deepl_api_key = "ec4c6a2a-efe7-39a2-2e61-1c5ab2f8558a:fx"

# Récupérer la date actuelle
date_actuelle_dd = datetime.now()

# Vérifier si l'heure est entre 0h et 6h
if date_actuelle_dd.hour >= 0 and date_actuelle_dd.hour < 6:
  # Si oui, changer la date actuelle en la veille
  date_actuelle_dd = date_actuelle_dd - timedelta(days=1)

# Formater la date actuelle dans le format spécifié
date_actuelle = date_actuelle_dd.strftime("%Y-%m-%d")


def get_api_data(date=None):
  """
  Fonction qui permet de récupérer les données de l'API APOD de la NASA 
  suivant une certaine date ou la date du jour si aucune date n'est spécifiée

  Dépendances:
    - requests

  Entrées:
  (string) date: date de l'image à récupérer, arguement optionnel

  Sortie:
  (json) données de l'image APOD à la date indiquée
  """

  api_url = "https://api.nasa.gov/planetary/apod?api_key=" + nasa_api_key

  if date:
    api_url += f"&date={date}"


  print(api_url)
  response = requests.get(api_url)

  if response.status_code == 200:
    return response.json()
  else:
    return None


def formatage_date(chaine_date):
  """
  Fonction convertissant une date au format "Année-Mois-Jour" 
  en "Jour de la semaine, Jour Mois Année

  """

  date_obj = datetime.strptime(chaine_date, "%Y-%m-%d")

  jours = [
      "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"
  ]

  # Le premier mois est vide pour que l'indexe soit entre 1 et 12 comme au format de notre date
  mois = [
      "", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet",
      "Août", "Septembre", "Octobre", "Novembre", "Décembre"
  ]

  jour_semaine = jours[date_obj.weekday()]
  jour = date_obj.day
  mois_str = mois[date_obj.month]
  annee = date_obj.year

  # Formater la date avec le bon format
  date_complete = f"{jour_semaine}, {jour} {mois_str} {annee}"

  return date_complete


app = Flask(__name__)


@app.route('/')
def index():
  date = request.args.get('date')
  api_data = get_api_data(date)

  if api_data is not None:

    # Parfois l'auteur de la photo n'est pas renseigné dans la réponse API
    auteur = api_data["copyright"] if "copyright" in api_data.keys() else ""

    # Parfois la source est une vidéo ou une intégration youtube ou autre chose qu'une         image, le code n'inclus pas ces cas
    if "hdurl" in api_data.keys():
      image_src = api_data["hdurl"]
    else:
      # Image par défaut fournie par la NASA
      image_src = "https://api.nasa.gov/planetary/apod/static/default_apod_image.jpg"

    date = formatage_date(api_data["date"])

    translator = deepl.Translator(deepl_api_key)

    trad_desc_raw = translator.translate_text(api_data["explanation"],
                                              target_lang="FR")
    trad_titre_raw = translator.translate_text(api_data["title"],
                                               target_lang="FR")
    is_today = (api_data["date"] == date_actuelle)

    return render_template('index.html',
                           image_src=image_src,
                           description=trad_desc_raw,
                           titre=trad_titre_raw,
                           auteur=auteur,
                           date=date,
                           is_today=is_today)
  else:
    return 'Erreur de requete api'


@app.route('/archives')
def archives():

  return render_template('archives.html', date_max=date_actuelle)


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=81, debug=True)
