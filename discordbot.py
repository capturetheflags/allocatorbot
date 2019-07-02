'''MIT License

Copyright (c) 2019 westiemcb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import aiohttp

import discord
from discord.ext import commands

from allocatorbot import AllocatorBot


class DiscordBot(commands.Bot):
    def __init__(self, credentials, *args, **options):
        super().__init__(command_prefix=self._get_prefixes, description='myAllocator scrape bot'
                          ,game=discord.Game(name='Minecraft'))
        self.session = None
        self.ab = None
        self.add_command(self.bot_exit)
        self.add_command(self.check_allocator)
        self.credentials = credentials
    
    def _get_prefixes(self, _, message):
        prefixes = ['.', '?', '>']
        return commands.when_mentioned_or(*prefixes)(self, message)
    
    async def on_ready(self):
        self.session = aiohttp.ClientSession()
        self.ab = AllocatorBot(self.credentials, self.session)
        
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
