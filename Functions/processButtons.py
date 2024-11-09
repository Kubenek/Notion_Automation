from notion_client import Client
from Functions.updateXP import updatePageXP

def getPageXP(page):
    return page["properties"].get("XP", {}).get("number", 0) or 0

def processButtons(notion: Client, PLAYER_DATABASE_ID):

    query = notion.databases.query(PLAYER_DATABASE_ID)
    page_list = query["results"]

    for page in page_list:
        status = page["properties"]["XP Updated"]["checkbox"]

        if not status: continue

        newXP = getPageXP(page) + 20

        page_id = page["id"]

        updatePageXP(notion, page_id, newXP)
