import json

from discordbot import DiscordBot


CREDS = {}

with open('creds.json', 'r') as f:
            CREDS = json.loads(f.read())
            
        
db = DiscordBot(CREDS)
db.run(CREDS['token'])
