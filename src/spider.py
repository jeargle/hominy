# John Eargle
# 2015

import sys
import json

from bs4 import BeautifulSoup
# import nltk
import requests




if __name__=='__main__':

    url = 'http://www.python-requests.org/en/latest/'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    req = requests.get(url)
    print req.status_code
    print req.headers
    print req.encoding
    html_doc = req.text
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    # print soup.prettify()   # pretty print HTML
    print '*** Title:', soup.title
    print '*** hrefs:'
    for link in soup.find_all('a'):
        print ' ', link.get('href')

    # remove script elements
    [s.extract() for s in soup('script')]
    print '*** Text:'
    print soup.get_text()   # print page text
