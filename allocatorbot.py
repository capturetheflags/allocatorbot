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

class AllocatorEntry:
    def __init__(self, soup):
        self.name = soup.find('span', {'class':'Name'})
        self.description = soup.find('span', {'class':'Description'})
        self.nofurtherchoices = soup.find('span', {'class':'NoFurtherChoicesRequired'})
        self.furtherchoices = soup.find('span',{'class':
                                                    ['DescendantFurtherChoicesRequired',
                                                     'DirectFurtherChoicesRequired']})
        self.problem = soup.find('div', {'class':'ExistingProblemPanel'})
        self.has_problem = self.problem is not None
        self.problem_heading = ''
        self.problem_text = ''
        self.required = self.nofurtherchoices is None
        
        if self.required:
            if self.problem is not None:
                heading = self.problem.find('span', {'class':'heading'})
                reason = self.problem.find('span', {'class':'reason'})
                self.problem_heading = heading.text
                self.problem_text = reason.text
                
    def __str__(self):
        ret = None
        if self.required:
            ret = f'{self.name.text} {self.description.text} {self.furtherchoices.text} '\
                  f'{self.problem_heading} {self.problem_text}'.strip()
        else:
            ret = f'{self.name.text} {self.description.text} {self.nofurtherchoices.text}'
        return ret
            

class AllocatorBot:
    def __init__(self, data, session=None):
        self.session = session
        self.data = data

    async def get_courses(self):
        data = {
            '__VIEWSTATE':'',
            '__VIEWSTATEGENERATOR':'',
            '__SCROLLPOSITIONX':0,
            '__SCROLLPOSITIONY':0,
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':'',
            '__EVENTVALIDATION':'',
            'ctl00$MainContent$userName':self.data['username'],
            'ctl00$MainContent$password':self.data['password'],
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
            
            ret = [AllocatorEntry(course) for course in courses]
            return ret        
    
    async def run(self):
        result = '\n'.join(await self.get_courses())
        #print(result)
        await self.session.close()
