import pytz
import interactions
from interactions import Client, Intents, listen, Task, IntervalTrigger
from interactions import slash_command, SlashContext, Embed
from datetime import datetime, timedelta
import main
from game import hour_first_game_of_day
import json
import os
from dotenv import load_dotenv

load_dotenv()


bot_token = os.getenv("BOT_TOKEN")
channel_test_id = os.getenv("CHANNEL_TEST_ID")
channel_id=os.getenv("CHANNEL_ID")



send_hour = None

bot = Client(intents=Intents.DEFAULT)

@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")
    print("Connected!")


    

@listen()
async def on_message_create(event):
    if event.message.author.id == bot.user.id:
        return
    print(f"{event.message.author}: {event.message.content}")


""""
@Task.create(IntervalTrigger(seconds=10))
async def send_message_periodically():
    channel_id = 1197550128559566848
    channel = await bot.fetch_channel(channel_id)
    start_time = asyncio.get_event_loop().time()
    if channel:
        maintenant = datetime.utcnow()
        heure_formattee = maintenant.strftime("%H:%M:%S")
        await channel.send(f"Maintenant : {heure_formattee}")
        elapsed_time = asyncio.get_event_loop().time() - start_time
        await asyncio.sleep(max(1 - elapsed_time % 1, 0))
    else:
        print("Channel not found")
"""


@slash_command(
    name="heure",
    description="Affiche l'heure actuelle",
    group_name="",
    group_description="",
    sub_cmd_name="",
    sub_cmd_description="",
)
async def my_command_function(ctx: SlashContext):
    maintenant_utc = datetime.utcnow()
    
    fuseau_horaire_france = pytz.timezone("Europe/Paris")
    maintenant_france = maintenant_utc.replace(tzinfo=pytz.utc).astimezone(fuseau_horaire_france)
    
    heure_formattee = maintenant_france.strftime("%H:%M:%S")
    await ctx.respond(f"Maintenant en France : {heure_formattee}")



async def sepration_between_games(channel):
    #taille d'une conversation discord

    embed = Embed(description="-------------------------------------------------------------------------------------")
    await channel.send(embed=embed)

async def send_formatted_list(channel, title, player_list):
    if not player_list:
        await channel.send(f"**{title}**: None")
        return

    messages_to_send = []
    current_message = f"**{title}**\n"
    
    for player in player_list:
        # Vérifier si le message actuel atteint la limite de caractères
        if len(current_message) + len(f"- {player}\n") > 2000:
            messages_to_send.append(current_message)
            current_message = f"**{title}** (suite):\n"

        current_message += f"- {player}\n"

    if current_message.strip() != "":
        messages_to_send.append(current_message)

    # Envoyer les messages
    for message in messages_to_send:
        embed = Embed(description=message)
        await channel.send(embed=embed)



@listen()
async def on_startup():
    global send_hour
    print("Connected!")
    
    try:
        channel = await bot.fetch_channel(channel_id)  
    except:
        print("Channel not found")
    """if channel:
        await channel.send("Hello, World!")"""
    
    #fonction de test envoyant un message toutes les 10 secondes
    #send_message_periodically.start() 

    while True:
        date=datetime.now()
        heure_formattee = date.strftime("%H:%M:%S")
        if heure_formattee== "15:00:00":
            main.main()
            first_game=hour_first_game_of_day()
            current_time = datetime.strptime(first_game, "%H:%M:%S")

            new_time = current_time + timedelta(hours=5)

            send_hour = new_time.strftime("%H:%M:%S")

            if(send_hour[0]=='0'):
                send_hour="23:00:00"
            list_out=main.list_player_out
            list_probable=main.list_player_probable
            list_questionable=main.list_player_questionable
            list_player_doubtful=main.list_player_doubtful
            list_note=main.list_player_note

        if heure_formattee==send_hour:

            # boucle parcourant games_day.json et qui affiche la balise Name de chaque match
            with open('games_day.json', 'r', encoding='utf-8') as json_file:
                game_data = json.load(json_file)

            header_embed = Embed(title="📅  Today's Game :", color=0x00FF00)
            await channel.send(embed=header_embed)
            game_list=[]
            for game in game_data:
                game_embed = Embed(title=f"🏀  {game['name']}", color=0x4286f4)
                await channel.send(embed=game_embed)
                game_list.append(game['name'])
            injury_embed = Embed(title="🩹  Injuries today :", color=0xFF0000)
            await channel.send(embed=injury_embed) 
            number_of_game=main.number_of_game()

            for opposition in game_list:
                list_o=[]
                list_p=[]
                list_q=[]
                list_d=[]
                list_n=[]
                for player in list_out:
                    team=player.split('(')[1].split(')')[0]
            
                    if opposition.find(team)!=-1:
                        list_o.append(player)
                for player in list_probable:
                    team=player.split('(')[1].split(')')[0]
                    if opposition.find(team)!=-1:
                        list_p.append(player)

                for player in list_questionable:
                    team=player.split('(')[1].split(')')[0]
                    if opposition.find(team)!=-1:
                        list_q.append(player)

                for player in list_player_doubtful:
                    team=player.split('(')[1].split(')')[0]
                    if opposition.find(team)!=-1:
                        list_d.append(player)

                for player in list_note:
                    team=player.split('(')[1].split(')')[0]
                    if opposition.find(team)!=-1:
                        list_n.append(player)

                if len(list_o)!=0:
                    await send_formatted_list(channel, "Game : "+opposition+"\r\n ❌ Out : ", list_o)
                if len(list_p)!=0:
                    await send_formatted_list(channel, "🤞 Probable for the game : ", list_p)
                if len(list_q)!=0:
                    await send_formatted_list(channel, "❓ Questionable for the game : ", list_q)
                if len(list_d)!=0:
                    await send_formatted_list(channel, "🤔 Doubtful for the game : ", list_d)
                if len(list_n)!=0:
                    await send_formatted_list(channel, "Other : ", list_n)
                await sepration_between_games(channel)
            await channel.send("@everyone")
            
        
        

    

if __name__ == "__main__":
    print("Starting bot...")
    bot.start(bot_token)