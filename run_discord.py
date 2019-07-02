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

#run the discord client and allocator scraping bot together

import json

from discordbot import DiscordBot


data = {}

'''

expects a file called "data.json" in your working directory
with format of
{
    "username": YOURVUWUSERNAME,
    "password": YOURVUWPASSWORD,
    "token": YOURDISCORDTOKEN,
    "channel": CHANNELID
}

'''
with open('data.json', 'r') as f:
            data = json.loads(f.read())
            
        
db = DiscordBot(data)
db.run(data['token'])
