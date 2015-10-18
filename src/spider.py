# John Eargle
# 2015

import sys
import json

from bs4 import BeautifulSoup
# import nltk
import requests



class RedditCheck:

    def __init__(self, username):
        self.username = username
        self.url = 'http://www.reddit.com/user/' + username

        
class GithubCheck:

    def __init__(self, username):
        self.username = username
        self.url = 'http://github.com/' + username


class CrunchBaseCheck:

    def __init__(self, name=None, org=None):
        self.name = name
        self.org = org
        
        if name is not None:
            self.name_url = 'http://www.crunchbase.com/person/' + name + '#/entity'
        if org is not None:
            self.org_url = 'http://www.crunchbase.com/organization/' + org + '#/entity'

        
class Generic:

    def __init__(self, url):
        self.url = url

        req = requests.get(url)
        print req.status_code
        print req.headers
        print req.encoding
        html_doc = req.text
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        
    def title(self):
        print '*** Title:', self.soup.title

    def hrefs(self):
        print '*** hrefs:'
        for link in self.soup.find_all('a'):
            print ' ', link.get('href')

    def text(self):
        print '*** Text:'
        print self.soup.get_text()   # print page text

    def kill_scripts(self):
        # remove script elements
        [s.extract() for s in self.soup('script')]

            
        
if __name__=='__main__':

    url = 'http://www.python-requests.org/en/latest/'
    if len(sys.argv) > 1:
        url = sys.argv[1]

    g = Generic(url)
    g.title()
    g.hrefs()
    g.kill_scripts()
    g.text()
