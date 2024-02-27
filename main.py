from injury import injury_html_to_json, isolate_team_injury
from game import game_html_to_json, game_day_html_to_json
import datetime
import json


list_player_out=[]
list_player_questionable=[]
list_player_probable=[]
list_player_doubtful=[]
list_player_note=[]

# Extract the injuries from the JSON file and put them in the corresponding list
def extract_out_players():
    global list_player_out
    global list_player_questionable
    global list_player_probable
    global list_player_note
    with open('today_injuries.json', 'r', encoding='utf-8') as json_file:
        player_injury_data = json.load(json_file)
    
    for team_data in player_injury_data:
        for player_info in team_data:
            player_and_team = f"{player_info['Player']} ({player_info['Team']})"
            if "Out" in player_info["Injury Note"]:
                list_player_out.append(player_and_team)
            elif "questionable" in player_info["Injury Note"]:
                list_player_questionable.append(player_and_team)
            elif "probable" in player_info["Injury Note"]:
                list_player_probable.append(player_and_team)
            elif "doubtful" in player_info["Injury Note"]:
                list_player_doubtful.append(player_and_team)
            else:
                player_team_note=f"{player_and_team} : {player_info['Injury Note']}"
                list_player_note.append(player_team_note)
            


def main():
    global list_player_other
    today_team=team_list()
    injury_html_to_json()

    player_injury=[]
    for team in today_team:
        player_injury.append(isolate_team_injury(team))
    
    with open('today_injuries.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(player_injury, indent=2, ensure_ascii=False))
    
    extract_out_players()




def number_of_game():
    game_day_html_to_json()
    try:
        with open('games_day.json', 'r', encoding='utf-8') as games_day_file:
            games_day_data = json.load(games_day_file)
    except FileNotFoundError:
        print("Fichier games_day.json non trouvé.")
        return []

    return len(games_day_data)



def team_list():
    game_day_html_to_json()
    try:
        with open('games_day.json', 'r', encoding='utf-8') as games_day_file:
            games_day_data = json.load(games_day_file)
    except FileNotFoundError:
        print("Fichier games_day.json non trouvé.")
        return []

    team_list = []
    for game in games_day_data:
        competitors = game.get('competitor', [])
        for team in competitors:
            team_name = team.get('name', '')
            if team_name:
                team_list.append(team_name)

    return team_list


if __name__ == "__main__":
    main()
   