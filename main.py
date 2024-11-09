
# * Imports ------------------]

import logging
import pytz
import os
import schedule
import time
import sys
import sqlite3

from colorama import Fore, Style
from datetime import datetime, timedelta
from dotenv import load_dotenv
from notion_client import Client
from Functions.resetQuests import resetQuests
from Functions.updateXP import applyXP
from Functions.displayStats import displayStats
from Functions.processButtons import processButtons
from QoL import printException

local_tz = pytz.timezone('Europe/Warsaw')

# * Database setup ----------------------]

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS statistics (
               sID INTEGER PRIMARY KEY UNIQUE,
               quests_completed INTEGER
    );
""")

cursor.execute("""
INSERT INTO statistics (sID, quests_completed)
               SELECT 0, 0
               WHERE NOT EXISTS (SELECT 1 FROM statistics WHERE sID = 0);
""")

conn.commit()
conn.close()

# * Console log setup ----------------]

class NoHttpRequestsFilter(logging.Filter):
    def filter(self, record):
        return 'HTTP Request' not in record.getMessage()

try:

    logging.getLogger("notion_client").setLevel(logging.WARNING)

    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler("console.log")

    console_handler.addFilter(NoHttpRequestsFilter())
    file_handler.addFilter(NoHttpRequestsFilter())

    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[file_handler, console_handler
        ])

    print = logging.info

    current_time = datetime.now()
    formatted_time = current_time.strftime("%d/%m/%Y, %H:%M:%S")

    print(f"{Style.RESET_ALL}{Fore.YELLOW}] {Style.RESET_ALL}{formatted_time} {Style.RESET_ALL}{Fore.BLUE}[INFO]{Style.RESET_ALL}{Fore.MAGENTA}         console.setup{Style.RESET_ALL} Console logging is ready to go!")

except Exception as e:
    printException(e)

# * Loading api keys ---------------]

try:

    load_dotenv('config.env')
    API_KEY = os.getenv("NOTION_API_KEY")
    QUEST_DATABASE_ID = os.getenv("QUEST_DATABASE_ID")
    PLAYER_DATABASE_ID = os.getenv("PLAYER_DB_ID")
    notion = Client(auth=API_KEY)

    current_time = datetime.now()
    formatted_time = current_time.strftime("%d/%m/%Y, %H:%M:%S")

    print(f"{Style.RESET_ALL}{Fore.YELLOW}] {Style.RESET_ALL}{formatted_time} {Style.RESET_ALL}{Fore.BLUE}[INFO]{Style.RESET_ALL}{Fore.MAGENTA}         notion.setup{Style.RESET_ALL} Notion client is setupped and ready to go!")

except Exception as e:
    printException(e)

# * Functions ----------------]

def schedule_jobs():
    local_time = datetime.now(local_tz)
    schedule_time = local_time.replace(hour=1, minute=0, second=0, microsecond=0)

    if local_time > schedule_time:
        schedule_time += timedelta(days=1)

    utc_schedule_time = schedule_time.astimezone(pytz.utc)

    schedule.every().day.at(utc_schedule_time.strftime("%H:%M")).do(reset_job)

def reset_job():
    try:
        resetQuests(notion, QUEST_DATABASE_ID)
        displayStats()
    except Exception as e:
        printException(e)

def update_job():
    try:
        applyXP(notion, QUEST_DATABASE_ID, PLAYER_DATABASE_ID)
    except Exception as e:
        printException(e)

def button_job():
    try:
        processButtons(notion, PLAYER_DATABASE_ID)
    except Exception as e:
        printException(e)

# * Main code --------------]

try:
    schedule_jobs()
    schedule.every(3).hours.do(update_job)
    schedule.every(30).minutes.do(button_job)

    while True:
        schedule.run_pending()
        time.sleep(120)
        
except Exception as e:
    printException(e)
