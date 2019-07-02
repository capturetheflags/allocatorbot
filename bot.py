import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

LOGIN_PAGE = 'https://student-sa-odd.victoria.ac.nz/Authentication/Login.aspx?ReturnUrl=%2fStudent.aspx'


with open('creds.json', 'r') as f:
    creds = json.loads(f.read())
    


async def main():
    data = {
        '__VIEWSTATE':'',
        '__VIEWSTATEGENERATOR':'',
        '__SCROLLPOSITIONX':0,
        '__SCROLLPOSITIONY':0,
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__EVENTVALIDATION':'',
        'ctl00$MainContent$userName':creds['username'],
        'ctl00$MainContent$password':creds['password'],
        'ctl00$MainContent$doLogin':'Login',
    }
    print(data)
    session = aiohttp.ClientSession()
    async with await session.get(LOGIN_PAGE) as response:
        print(await response.text())
    await session.close()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
