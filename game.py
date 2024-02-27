import requests
from bs4 import BeautifulSoup
import json
import datetime



# Create a JSON file with all the games of the current month
def game_html_to_json():

    now = datetime.datetime.now()
    month = now.strftime("%B").lower()
    url = f"https://www.basketball-reference.com/leagues/NBA_2024_games-{month}.html"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        script_tag = soup.find('script', {'type': 'application/ld+json'})
    
        if script_tag:
            json_data = json.loads(script_tag.string)
            open('all_games.json', 'w', encoding='utf-8').write(json.dumps(json_data, indent=2, ensure_ascii=False))
        
        
        else:
            print("Script JSON non trouvé dans la page HTML.")

    else:
        print(f"Échec de la requête. Code de statut : {response.status_code}")


# Get the hour of the first game of the day
def hour_first_game_of_day():
    date = datetime.datetime.now()
    date_formatted = date.strftime("%Y-%m-%d")
    url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{date_formatted}?key=83595eb4708744e2ab3930eb8d03b73e"

    response = requests.get(url)

    if response.status_code == 200:
        json_data = json.loads(response.text)

        if json_data and len(json_data) > 0:

            first_game_datetime = json_data[0].get("DateTime")

            if first_game_datetime:
                first_hour=first_game_datetime.split('T')[1]
            else:
                print("Clé 'DateTime' non trouvée dans le premier jeu.")
        else:
            print("Aucun jeu trouvé pour la date spécifiée.")
    else:
        print(f"Échec de la requête. Code de statut : {response.status_code}")
    return first_hour


def game_day_html_to_json():
    game_html_to_json()
    try:
        with open('all_games.json', 'r', encoding='utf-8') as all_games_file:
            all_games_data = json.load(all_games_file)
    except FileNotFoundError:
        print("Fichier all_games.json non trouvé.")
        return

    # Get the current date in the format "Mon, Jan 1, 2022"
    today = datetime.datetime.now().strftime("%a, %b %-d, %Y")
    
    games_today = [game for game in all_games_data if game.get('startDate') == today]

    with open('games_day.json', 'w', encoding='utf-8') as games_day_file:
        json.dump(games_today, games_day_file, indent=2, ensure_ascii=False)


game_day_html_to_json()





