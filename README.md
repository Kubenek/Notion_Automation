
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



## FAQ

#### What is this project?

If you didn't catch it, here's a detailed explanation. 
This is an automation script written in python. It automates a few processes, with the main focus on applying XP from completed quests.

I have a dashboard in notion with a database for Quests. These so called quests have xp, so after one is completed and the script picks up on it, it updates my other databases' XP. The database has pages for my main profile & for knowledge profiles (ex. Programming, Math).

It's basically a script to automate a RPG game in notion, hope you get it.

#### Is this free?

For the most part. Python and Notion are free, the problem is hosting.

You could run in locally through a terminal (ex. VS Code), but you need to keep your machine on, which isn't viable in the long run. If you have a server then that's great.

No worries, the internet also has some free hosting websites. I'm using SillyDev (really good ngl), but you could also checkout PylexNodes, also worked pretty well. In general, if you have any website to host python scripts then this is gonna work.



