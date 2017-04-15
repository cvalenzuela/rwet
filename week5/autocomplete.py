
# coding: utf-8

# Get Ulysess(4300) from gutenberg and select a random set of sentences.

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from random import choice

text = strip_headers(load_etext(4300)).strip()
text = text.split('.')

amount_of_sentences = 10
sentences = []

valid = False

# get the first 4 words of a random sentence
for sentence in range(amount_of_sentences):
    while not valid:
        sentence = choice(text)
        valid = len(sentence.split()) > 4 and len(sentence.split()) < 10
    sentence = sentence.rstrip()
    sentence = sentence.lstrip()
    sentence = sentence.replace('\n', ' ')
    sentences.append(sentence+'.')
    valid = False

print sentences

# use googles autocomplete api to load autocomplete sentences
# http://suggestqueries.google.com/complete/search?client=firefox&q=QUERY

import urllib
import sys
import json

url = "http://suggestqueries.google.com/complete/search?"

amount_of_words = 2
final_result = []

# look for the suggested queries and load a random one based on the input text
for sentence in sentences:
    words = ' '.join(sentence.split()[:amount_of_words])
    query = urllib.urlencode({"client": "firefox", "q": words})
    search_term = url + query
    try:
        urlobj = urllib.urlopen(search_term)
        result = json.loads(urlobj.read())
        if len(result[1]) > 1:
            print '<span>' + sentence + '</span><br/>'
            print '<span>' + choice(result[1]).capitalize()+'.' + '</span><br/>'
        else:
            print 'nop'
    except:
        print 'Format not valid for query. Maybe the string has wierd James Joyce characters.'
