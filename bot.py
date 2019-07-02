import aiohttp
from bs4 import BeautifulSoup
import json

with open("creds.json", "r") as f:
    data = json.loads(f.read())
    
print(data)
