#!/usr/bin/python
from __future__ import unicode_literals # allows to use unicode strings
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory, render_template
import markov
import json
import spacy
from random import choice, randint

# spacy
import spacy
nlp = spacy.load('en')

# set up flask app
app = Flask(__name__)
app.debug = True

#metamorphosis, shakespear , gutenberg, darwin
text = open('source_text/gutenberg.txt').read().lower()
text = text.split()
model = markov.build_model(text, 1)

# Main Route
@app.route("/")
def index():
    return render_template('index.html')

# markov version
@app.route('/_markov')
def markovme():
    instructions = []
    routes = json.loads(request.args['routes'])
    print(routes)
    for route in routes:
        seed = route["instruction"].split()[:1]
        line = " ".join(markov.generate(model, 1, seed))
        doc = nlp(line)
        nouns = [item.text for item in doc if item.pos_ == 'NOUN']
        adjs = [item.text for item in doc if item.pos_ == 'ADJ']
        while(len(line) > 110):
            if(randint(1,10) > 9):
                line = line.partition(choice(nouns))[0] + choice(nouns)
                line = " ".join(line.split()).capitalize().partition(".")[0] + '.'
            else:
                line = line.partition(choice(adjs))[0] + choice(adjs)
                line = " ".join(line.split()).capitalize().partition(".")[0] + '.'
        instructions.append(line)
    return jsonify(status='success', result=instructions);

# Run the server
if __name__ == "__main__":
    app.run()
    #app.run( host='0.0.0.0', port=8080, debug=False )
