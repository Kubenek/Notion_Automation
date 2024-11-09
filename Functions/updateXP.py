from colorama import Fore, Style
from Functions.animate import animate
import threading
from datetime import datetime
from QoL import printException
import time
import sqlite3

def findCompletedQuestList(quest_list):
    cQuestList = []
    for quest in quest_list:
        status = quest["properties"]["Status"]["status"]["name"]
        if status == "Done":
            cQuestList.append(quest)
        else: continue

    return cQuestList

def getQuestValues(quest):
    newPXP = quest["properties"]["Next pXP"]["formula"]["number"]
    newEXP = quest["properties"]["Next eXP"]["formula"]["number"]
    knowledgeName = quest["properties"]["Experience"]["select"]["name"]

    return newPXP, newEXP, knowledgeName

def getPlayerValues(player):
    knowledgeName = player["properties"]["Name"]["title"][0]["text"]["content"]
    return knowledgeName

def finishAnimation(animation_thread, start_time):
    animation_thread.join()
    end_time = time.time()
    exec_time = end_time - start_time
    exec_time = round(exec_time, 2)

    return animation_thread, exec_time

def updatePageXP(notion, page_id, newXP):
    notion.pages.update(page_id=page_id,properties={"XP": {"number": newXP}})

def setQuestStatus(notion, quest_id, status):
    notion.pages.update(page_id=quest_id,properties={"Status": {"status": {"name": f"{status}"}}})

def applyXP(notion, QUEST_DATABASE_ID, PLAYER_DATABASE_ID):
    done = [False]
    try:
        start_time = time.time()
        query = notion.databases.query(QUEST_DATABASE_ID)
        quest_list = query["results"]
        query = notion.databases.query(PLAYER_DATABASE_ID)
        player_list = query["results"]

        playerId = len(player_list) - 1
		
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d/%m/%Y %H:%M:%S")
        
        amount = 0

        global animation_thread
        animation_thread = threading.Thread(target=animate, args=(done, f"{Style.RESET_ALL}{Fore.YELLOW}] {Style.RESET_ALL}{formatted_time} {Style.RESET_ALL}{Fore.BLUE}[INFO]{Style.RESET_ALL}{Fore.MAGENTA}         xp.update{Style.RESET_ALL} XP update in progress:"))

        animation_thread.start()
        
        cQuestList = findCompletedQuestList(quest_list)

        for quest in cQuestList:

            player_id = player_list[playerId]["id"]
            quest_id = quest["id"]

            newPXP, newEXP, knowledgeName = getQuestValues(quest)

            updatePageXP(notion, player_id, newPXP)
            setQuestStatus(notion, quest_id, "Archived")

            amount += 1

            for player in player_list:

                currentKnowledge = getPlayerValues(player)

                if currentKnowledge != knowledgeName: continue
                    
                experienceId = player["id"]
                updatePageXP(notion, experienceId, newEXP)
                break
            
        done[0] = True
        
        animation_thread, exec_time = finishAnimation(animation_thread, start_time)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE statistics SET quests_completed = quests_completed + ? WHERE sID = 0;", (amount,))
        
        conn.commit()
        conn.close()

        print(f'\n{Style.RESET_ALL}{Fore.YELLOW}] {Style.RESET_ALL}{formatted_time}{Style.RESET_ALL}{Fore.GREEN} [SUCCESS]      {Style.RESET_ALL}{Fore.MAGENTA}xp.update{Style.RESET_ALL} Succesfully finished the XP addition process in {Fore.BLUE}{exec_time}{Style.RESET_ALL} seconds! Applied xp from {amount} quests!')

    except Exception as e:
        done[0] = True
        if 'animation_thread' in locals():
            animation_thread.join()
        printException(e)
    