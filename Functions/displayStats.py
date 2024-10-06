import sqlite3

from QoL import printException

def displayStats():
    try:

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT quests_completed FROM statistics WHERE sID = 0;")
        result = cursor.fetchone()

        print(f"Quests completed: {result}")

    except Exception as e:
        printException(e)