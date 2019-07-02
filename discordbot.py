'''
MIT License

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

# class implementing super basic discord bot functionality

import aiohttp

import discord
from discord.ext import commands, tasks

from allocatorbot import AllocatorBot


class DiscordBot(commands.Bot):
    def __init__(self, data, *args, **options):
        super().__init__(command_prefix=self._get_prefixes, description='myAllocator scrape bot'
                          ,game=discord.Game(name='Minecraft'))
        self.session = None
        self.ab = None
        self.add_command(self.bot_exit)
        self.add_command(self.check_allocator)
        self.add_command(self.add_allocator_role)
        self.data = data
        self.allocator_channel = data['channel']
        self.allocator_role = None
    
    def _get_prefixes(self, _, message):
        prefixes = ['.', '?', '>']
        return commands.when_mentioned_or(*prefixes)(self, message)
    
    async def on_ready(self):
        self.session = aiohttp.ClientSession()
        self.ab = AllocatorBot(self.data, self.session)
        self.check_allocator_task.start()
        self.allocator_channel = self.get_channel(self.allocator_channel)
        self.allocator_role = discord.utils.find(lambda r: r.name.lower() == 'allocator',
                                                 self.allocator_channel.guild.roles)
        if self.allocator_channel is None:
            print('Channel cannot be found with the specified ID.')
        elif self.allocator_role is None:
            print('There does not seem to be an allocator role set up in specified guild/channel')
        print('Ready')
        print(f'Current configuration:\nDiscord Client is {self.user}\nVUW allocator user is {self.data["username"]}')
        
    @commands.command(name='check')
    async def check_allocator(ctx):
        await ctx.send('Checking allocator...')
        result = '\n'.join([str(s) for s in await ctx.bot.ab.get_courses()])
        await ctx.send(f'```\n{result}```')
        
    @commands.command(name='role')
    async def add_allocator_role(ctx):
        if ctx.bot.allocator_role in ctx.author.roles:
            await ctx.author.remove_roles(ctx.bot.allocator_role)
            await ctx.send('Removed allocator role.')
        else:
            await ctx.author.add_roles(ctx.bot.allocator_role)
            await ctx.send('Gave allocator role.')
    
    @commands.command(name='exit', hidden=True)
    @commands.is_owner()
    async def bot_exit(ctx):
        try:
            await ctx.send('Exiting')
            ctx.bot.check_allocator_task.cancel()
        except (AttributeError, discord.Forbidden):
            pass
        await ctx.bot.session.close()
        await ctx.bot.logout()
        
    @tasks.loop(seconds=10)
    async def check_allocator_task(self):
        await self.allocator_channel.send('Checking allocator...')
        result = await self.ab.get_courses()
        for course in result:
            if course.required:
                if course.has_problem:
                    await self.allocator_channel.send(f'{course}')
                else:
                    await self.allocator_channel.send(f'{self.allocator_role.mention} {course}')
