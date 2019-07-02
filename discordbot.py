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
