# John Eargle
# 2015-2016

# Dependencies:
#   BeautifulSoup
#   nltk
#   requests
#   robotexclusionrulesparser - handles wildcards (unlike robotparser)

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
    """
    Base class for URL checkers.  Check a given URL for specific
    users and/or organizations.  The robots.txt files is grabbed
    and checked first in order to avoid banned pages.
    """

    def __init__(self, url_base, user_suffix='%s', org_suffix='%s'):
        self.url_base = url_base
        self.user_suffix = user_suffix
        self.org_suffix = org_suffix
        self.rp = None

    def check_user(self, user):
        if self.user_suffix is None:
            return None
        if self.rp is None:
            self.check_robots()

        url = (self.url_base + self.user_suffix) % (user)
        if not self.rp.can_fetch('*', url):
            return None

        req = requests.get(url)
        print 'url:', url
        print 'status:', req.status_code
        print 'headers:', req.headers
        print 'encoding:', req.encoding

    def check_org(self, org):
        if self.org_suffix is None:
            return None
        if self.rp is None:
            self.check_robots()

        url = (self.url_base + self.org_suffix) % (org)
        if not self.rp.can_fetch('*', url):
            return None

        req = requests.get(url)
        print 'url:', url
        print 'status:', req.status_code
        print 'headers:', req.headers
        print 'encoding:', req.encoding

    def check_robots(self):
        self.rp = rerp.RobotFileParserLookalike()
        self.rp.set_url(self.url_base + 'robots.txt')
        self.rp.read()


class RedditCheck(UrlCheck):
    """
    URL checker for reddit.
    """

    def __init__(self):
        UrlCheck.__init__(self, 'http://www.reddit.com/',
                          user_suffix='user/%s')


class TwitterCheck(UrlCheck):
    """
    URL checker for Twitter.
    """

    def __init__(self):
        UrlCheck.__init__(self, 'http://twitter.com/')


class GithubCheck(UrlCheck):
    """
    URL checker for GitHub.
    """

    def __init__(self):
        UrlCheck.__init__(self, 'http://github.com/')


class CrunchBaseCheck(UrlCheck):
    """
    URL checker for CrunchBase.
    """

    def __init__(self):
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

    if len(sys.argv) > 1:
        username = sys.argv[1]
        
    rc1 = RedditCheck()
    rc1.check_user(username)
    
    # tc1 = TwitterCheck()
    # gc1 = GithubCheck()
    # cbc1 = CrunchBaseCheck()

