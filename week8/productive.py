# -*- coding: utf-8 -*-
#!/usr/bin/python
from applescript import asrun, asquote, current_text, paste_text, linebreak
import markov
from random import choice, randint
import robobrowser
# Markov model
# http://www.decontextualize.com/teaching/rwet/n-grams-and-markov-chains/
# --------

supreme_conversations = open("data/supreme.conversations.txt")
movie_quotes = open("data/moviequotes.memorable_quotes.txt")

data = ""

for line in movie_quotes:
    line = line.strip()
    line = line.split('+++$+++')
    data+=line[-1]

words = data.split()
words[0:2]
model = markov.build_model(words, 2)
" ".join(markov.generate(model, 2, ['the', 'police']))

# get the current text
msword_text = asrun(current_text).split('\r')
decoded_text = []
for line in msword_text:
    decoded_text.append(line.decode('utf-8').lower())


for i in range(2):
    asrun(linebreak()) # add a new line and then begin writting

for line in decoded_text:
    if len(line) > 2:
        seed = line.split()[0:2]
        generated = markov.generate(model, 2, seed)
        generated = " ".join(generated[:randint(6,12)])
        asrun(linebreak())
        asrun(paste_text(generated)) # run the applescript to paste into msword
    else:
        asrun(paste_text(""))

print 'Thanks for being productive'
