#
# pip install beautifulsoup4 soupsieve
# pip install langdetect
#
from bs4 import BeautifulSoup as Soup
#from soupselect import select
import urllib
import requests

from urllib.parse import urlparse

def is_url(url):
    try:
        result = urlparse(url)
        #return all([result.scheme, result.netloc])
        return True
    except ValueError:
        return False

def request(url, ssl_verify=True):
    res = requests.get(url, data=params, verify=ssl_verify)
    return res.text

class Website:
    url = None
    content = ""
    dom = Soup('<div></div>')
    def __init__(self, url):
        if is_url(url):
            self.url = url
            self.content = request(self.url)
        else:
            self.content = url
        self.dom = Soup(content)
    def q(self, selector = 'h1'):
        return self.dom.select(selector)
    def select_text(self, selector = 'h1'):
        node = self.dom.select_one(selector)
        return node.text
    def links(self):
        for link in self.dom.find_all('a'):
            print(link.get('href'))
    def text(self):
        return self.dom.get_text()
    def article_text(self):
        return "TODO"
    def language(self):
        """ Returns en, de, ... """
        from langdetect import detect
        return detect(self.text())
        
# https://spacy.io/models/de
# import spacy
#from spacy.lang.en.examples import sentences 
#nlp = spacy.load("en_core_web_sm")
#doc = nlp(sentences[0])
#print(doc.text)
#for token in doc:
#    print(token.text, token.pos_, token.dep_)
#    import spacy
#from spacy.lang.de.examples import sentences 
#
#nlp = spacy.load("de_core_news_sm")
#doc = nlp(sentences[0])
#print(doc.text)
#for token in doc:
#    print(token.text, token.pos_, token.dep_)