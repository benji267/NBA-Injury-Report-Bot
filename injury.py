import requests
from bs4 import BeautifulSoup
import json
import datetime




def injury_html_to_json():
    # URL de la page HTML contenant les informations sur les blessures
    url = "https://www.basketball-reference.com/friv/injuries.fcgi"

    # Faire une requête GET à l'URL
    response = requests.get(url)

    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser la page HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Sélectionner toutes les lignes (tr) dans le tableau (tbody)
        rows = soup.select('tbody tr')

        # Créer une liste pour stocker les données des joueurs blessés
        player_injuries = []

        # Parcourir chaque ligne et extraire les informations nécessaires
        for row in rows:
            player_name = row.select_one('[data-stat="player"] a').text
            team_name = row.select_one('[data-stat="team_name"] a').text
            date_update = row.select_one('[data-stat="date_update"]').text
            injury_note = row.select_one('[data-stat="note"]').text

            # Ajouter les données dans la liste
            player_injury_data = {
                "Player": player_name,
                "Team": team_name,
                "Update Date": date_update,
                "Injury Note": injury_note
            }
            player_injuries.append(player_injury_data)

        # Convertir la liste en format JSON
        player_injuries_json = json.dumps(player_injuries, indent=2, ensure_ascii=False)

        # Écrire le JSON dans un fichier
        with open('player_injury.json', 'w', encoding='utf-8') as json_file:
            json_file.write(player_injuries_json)

    else:
        print(f"Échec de la requête. Code de statut : {response.status_code}")

def isolate_team_injury(team):
    injury_html_to_json()
    try:
        with open('player_injury.json', 'r', encoding='utf-8') as player_injury_file:
            player_injury_data = json.load(player_injury_file)
    except FileNotFoundError:
        print("Fichier player_injury.json non trouvé.")
        return []
    
    team_injury = []
    for player in player_injury_data:
        if player.get('Team') == team:
            team_injury.append(player)
    return team_injury

