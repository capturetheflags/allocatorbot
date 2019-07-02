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

# class implementing the allocator scraping functionality

import aiohttp
from bs4 import BeautifulSoup


LOGIN_URL = 'https://student-sa-odd.victoria.ac.nz/Authentication/Login.aspx?ReturnUrl=%2fStudent.aspx'

class AllocatorBot:
    def __init__(self, credentials, session=None):
        self.session = session
        self.credentials = credentials

    async def get_courses(self):
        data = {
            '__VIEWSTATE':'',
            '__VIEWSTATEGENERATOR':'',
            '__SCROLLPOSITIONX':0,
            '__SCROLLPOSITIONY':0,
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':'',
            '__EVENTVALIDATION':'',
            'ctl00$MainContent$userName':self.credentials['username'],
            'ctl00$MainContent$password':self.credentials['password'],
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
            for course in courses:
                print(course)
            
            
            ret = [course.text.strip() for course in courses]
            return ret        
    
    async def run(self):
        await self.get_courses()
        await self.session.close()
