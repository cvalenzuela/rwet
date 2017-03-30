# -*- coding: utf-8 -*-
# This is the original script
# https://github.com/cvalenzuela/rwet/tree/master/week5
# Cristóbal Valenzuela

import urllib
import json
from random import choice

def completme(sentence='I want', amount_of_words=3):

    url = "http://suggestqueries.google.com/complete/search?"
    final_result = []

    # look for the suggested queries and load a random one based on the input text
    words = ' '.join(sentence.split()[:amount_of_words])
    query = urllib.urlencode({"client": "firefox", "q": words})
    search_term = url + query

    try:
        urlobj = urllib.urlopen(search_term)
        result = json.loads(urlobj.read())
        if len(result[1]) > 1:
            result = choice(result[1]).capitalize().encode("utf-8")
            return ' ' + ' '.join(result.split()[3:])
            #return choice(result[1]).capitalize().encode("utf-8")
        else:
            return 'Nop'
    except:
        return 'Google does not want to autocomplete you'
