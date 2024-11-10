
# Notion Automation

Basically a notion quest automation done in python, uses notion-client library

It's pretty specific for my notion setup as it directly takes properties and values from set databases

## Authors

- [@Kubenek](https://github.com/Kubenek)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`NOTION_API_KEY`
`QUEST_DATABASE_ID`
`PLAYER_DB_ID`




## Documentation

not yet, maybe I'll make a tutorial on it someday


## Features

- On the end of the day resets all Daily Quests to the status of 'Not Started'
- Every 3 hours checks for any Quests with status 'Done', applies their XP and sets status to 'Archived'
- Any uncompleted Daily Quests have their xp depleted from players' XP pool
- Console & Error logging
- Tracks how many quests completed in a file 'database.db' using sqlite3


