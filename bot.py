import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import discord

LOGIN_URL = 'https://student-sa-odd.victoria.ac.nz/Authentication/Login.aspx?ReturnUrl=%2fStudent.aspx'
CREDS = {}

with open('creds.json', 'r') as f:
            CREDS = json.loads(f.read())
            
class AllocatorBot:
    def __init__(self):
        self.session = None


    async def get_courses(self):
        data = {
            '__VIEWSTATE':'',
            '__VIEWSTATEGENERATOR':'',
            '__SCROLLPOSITIONX':0,
            '__SCROLLPOSITIONY':0,
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':'',
            '__EVENTVALIDATION':'',
            'ctl00$MainContent$userName':CREDS['username'],
            'ctl00$MainContent$password':CREDS['password'],
            'ctl00$MainContent$doLogin':'Login',
        }

        self.session = aiohttp.ClientSession()
        async with await self.session.get(LOGIN_URL) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            form = soup.find('form', id='aspnetForm')           
            for k,v in data.items():
                if not v:
                    value = form.find('input', id=k)
                    if value is not None:
                        data[k] = value['value']
        
        async with await self.session.post(LOGIN_URL, data=data) as response:
            listing = BeautifulSoup(await response.text(), 'lxml')
            course_list = listing.find('ul', {'class':'TopNodes'})
            courses = course_list.find_all('div', {'class':'Ao Ao_MO Ao_1'})
            for course in courses:
                print(course.text.strip())
                    
    
    async def main(self):
        await self.get_courses()
        await self.session.close()
        
ab = AllocatorBot()
loop = asyncio.get_event_loop()
loop.run_until_complete(ab.main())
