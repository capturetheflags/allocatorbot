import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import discord
from discord.ext import commands

LOGIN_URL = 'https://student-sa-odd.victoria.ac.nz/Authentication/Login.aspx?ReturnUrl=%2fStudent.aspx'
CREDS = {}

with open('creds.json', 'r') as f:
            CREDS = json.loads(f.read())
            
class AllocatorBot:
    def __init__(self, session=None):
        self.session = session


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
        if not self.session:
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
            ret = [course.text.strip() for course in courses]
            return ret        
    
    async def run(self):
        await self.get_courses()
        await self.session.close()

class DiscordBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix=self._get_prefixes, description='myAllocator scrape bot'
                          ,game=discord.Game(name='Minecraft'))
        self.session = None
        self.ab = None
        self.add_command(self.bot_exit)
        self.add_command(self.check_allocator)
    
    def _get_prefixes(self, _, message):
        prefixes = ['.', '?', '>']
        return commands.when_mentioned_or(*prefixes)(self, message)
    
    async def on_ready(self):
        self.session = aiohttp.ClientSession()
        self.ab = AllocatorBot(self.session)
        
    @commands.command(name='check')
    async def check_allocator(ctx):
        await ctx.send('Checking allocator...')
        result = '\n'.join(await ctx.bot.ab.get_courses())
        await ctx.send(f'```\n{result}```')
    
    @commands.command(name='exit', hidden=True)
    @commands.is_owner()
    async def bot_exit(ctx):
        try:
            await ctx.send('Exiting')
        except (AttributeError, discord.Forbidden):
            pass
        await ctx.bot.session.close()
        await ctx.bot.logout()
        
db = DiscordBot()
db.run(CREDS['token'])
