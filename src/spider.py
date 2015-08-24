# John Eargle
# 2015

import sys
import json

from bs4 import BeautifulSoup
import requests


req = requests.get('http://www.python-requests.org/en/latest/')
print req.status_code
print req.headers
print req.encoding
html_doc = req.text

soup = BeautifulSoup(html_doc, 'html.parser')
# print soup.prettify()   # pretty print HTML
print 'title:', soup.title
for link in soup.find_all('a'):
    print link.get('href')

print soup.get_text()   # print page text
