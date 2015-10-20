# John Eargle
# 2015

# Dependencies:
#   BeautifulSoup
#   nltk
#   requests
#   robotexclusionrulesparser

import sys
import json

from bs4 import BeautifulSoup
# import nltk
import requests
import robotexclusionrulesparser as rerp


class GenericUrl:

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


class UrlCheck:

    def __init__(self, url_base, user_suffix='%s', org_suffix='%s'):
        self.url_base = url_base
        self.user_suffix = user_suffix
        self.org_suffix = org_suffix

    def check_user(self, user):
        if self.user_suffix is None:
            return None
        
        url = (self.url_base + self.user_suffix) % (user)
        req = requests.get(url)
        print 'url:', url
        print 'status:', req.status_code
        print 'headers:', req.headers
        print 'encoding:', req.encoding

    def check_org(self, org):
        if self.org_suffix is None:
            return None

        url = (self.url_base + self.org_suffix) % (org)
        req = requests.get(url)
        print 'url:', url
        print 'status:', req.status_code
        print 'headers:', req.headers
        print 'encoding:', req.encoding

    def check_robots(self):
        rp = rerp.RobotFileParserLookalike()
        rp.set_url(self.url_base + 'robots.txt')
        rp.read()
        rp.can_fetch('*', self.url_base + 'blah')
        rp.can_fetch('*', self.url_base + 'moo.xml')
        

class RedditCheck(UrlCheck):

    def __init__(self):
        UrlCheck.__init__(self, 'http://www.reddit.com/',
                          user_suffix='user/%s')

        
class GithubCheck(UrlCheck):

    def __init__(self):
        UrlCheck.__init__(self, 'http://github.com/')


class CrunchBaseCheck(UrlCheck):

    def __init__(self, username=None, org=None):
        UrlCheck.__init__(self, 'http://www.crunchbase.com/',
                          user_suffix='person/%s#/entity',
                          org_suffix='organization/%s#/entity')
        


if __name__=='__main__':

    # url = 'http://www.python-requests.org/en/latest/'
    # if len(sys.argv) > 1:
    #     url = sys.argv[1]

    # g = GenericUrl(url)
    # g.title()
    # g.hrefs()
    # g.kill_scripts()
    # g.text()

    rc1 = RedditCheck()
    ghc1 = GithubCheck()

    
