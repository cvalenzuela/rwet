# -*- coding: utf-8 -*-
#!/usr/bin/python
from applescript import asrun, asquote, current_text, paste_text, linebreak
import markov
from random import choice, randint

# Markov model
# http://www.decontextualize.com/teaching/rwet/n-grams-and-markov-chains/
# --------

supreme_conversations = open("data/supreme.conversations.txt").read().split()
movie_quotes = open("data/moviequotes.memorable_quotes.txt").read().split()

model = markov.build_model(supreme_conversations, 2)
#generated = markov.generate(model, 2, ["this", "is"])

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
# paste the generated markov chain
#paste = asrun(paste_new_text)
