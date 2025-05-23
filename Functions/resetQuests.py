from colorama import Fore, Style
from Functions.animate import animate
import threading
from datetime import datetime
from QoL import printException
from Functions.updateXP import updatePageXP
import time

def get_exec_time(start_time, end_time):
    exec_time = end_time - start_time
    exec_time = round(exec_time, 2)
    return exec_time

def getPlayerID(notion, PLAYER_DATABASE_ID):
    query = notion.databases.query(PLAYER_DATABASE_ID)
    player_list = query["results"]
    playerId = len(player_list) - 1
    return player_list[playerId]["id"]

def resetQuests(notion, QUEST_DATABASE_ID, PLAYER_DATABASE_ID):
    done = [False]
    try:
        start_time = time.time()
        query = notion.databases.query(QUEST_DATABASE_ID)
        quest_list = query["results"]

        current_time = datetime.now()
        formatted_time = current_time.strftime("%d/%m/%Y, %H:%M:%S")

        global animation_thread
        animation_thread = threading.Thread(target=animate, args=(done, f"{Style.RESET_ALL}{Fore.YELLOW}] {Style.RESET_ALL}{formatted_time} {Style.RESET_ALL}{Fore.BLUE}[INFO]{Style.RESET_ALL}{Fore.MAGENTA}         quest.reset{Style.RESET_ALL} Quest reset in progress:"))

        animation_thread.start()

        total_xp = 0

        for quest in quest_list:
            status = quest["properties"]["Status"]["status"]["name"]
            type = quest["properties"]["Type"]["select"]["name"]

            if status == "Not started" and type == "Daily Quest":
                quest_xp = quest["properties"]["XP Reward"]["number"]
                
                total_xp-=quest_xp

                continue

        for quest in quest_list:

            status = quest["properties"]["Status"]["status"]["name"]
            type = quest["properties"]["Type"]["select"]["name"]
            
            quest_id = quest["id"]

            if status == "Archived" and type == "Quest":
                notion.pages.update(page_id=quest_id, archived=True)
            else:
                notion.pages.update(page_id=quest_id,properties={"Status": {"status": {"name": "Not started"}}})


        query = notion.databases.query(PLAYER_DATABASE_ID)
        player_list = query["results"]
        player_id = getPlayerID(notion, PLAYER_DATABASE_ID)
        playerId = len(player_list) - 1
        player_xp = player_list[playerId]["properties"]["XP"]["number"]
        player_xp+=total_xp
        updatePageXP(notion, player_id, player_xp)

        done[0] = True
        animation_thread.join()
        end_time = time.time()

        exec_time = get_exec_time(start_time, end_time)

        current_time = datetime.now()
        formatted_time = current_time.strftime("%d/%m/%Y, %H:%M:%S")

        print(f'\n{Style.RESET_ALL}{Fore.YELLOW}] {Style.RESET_ALL}{formatted_time}{Style.RESET_ALL}{Fore.GREEN} [SUCCESS]      {Style.RESET_ALL}{Fore.MAGENTA}quest.reset{Style.RESET_ALL} Succesfully completed the quest reset in {Fore.BLUE}{exec_time}{Style.RESET_ALL} seconds!')

    except Exception as e:
        done[0] = True
        if 'animation_thread' in locals():
            animation_thread.join()
        printException(e)
    