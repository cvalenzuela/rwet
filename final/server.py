#!/usr/bin/python
from __future__ import unicode_literals # allows to use unicode strings
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory, render_template
from random import choice, sample
from instructions import generate_instructions
import json

import keras
from keras.models import load_model
import numpy as np
from random import choice, randint
import markov

# spacy
import spacy
nlp = spacy.load('en')

# set up flask app
app = Flask(__name__)
app.debug = False

#metamorphosis, shakespear , gutenberg, darwin
source = 'gutenberg'
model = load_model('models/' + source + '.h5')
text = open('source_text/'  + source + '.txt').read().lower()  # read the file and convert to lowercase
maxlen = 40
chars = sorted(list(set(text)))
# what position does each character exist at in the prev list
char_indices = dict((c,i) for i, c in enumerate(chars))
indices_char = dict((i,c) for i,c in enumerate(chars))

# markov config
words = text.split()
markov_model = markov.build_model(words, 2)

# helper function to sample an index from a probability array
def sample(preds, temperature=0.1):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# Main Route
@app.route("/")
def index():
    return render_template('index.html')

# Generate knn text
@app.route('/_knn')
def add_numbers():
    routes = json.loads(request.args['routes'])
    text = generate_instructions(routes)
    return jsonify(status='success', result=text)

# Generate LSTM text
@app.route('/_lstm')
def upload():
    instructions = []
    routes = json.loads(request.args['routes'])
    diversity = float(0.3)
    length = int(100)

    for route in routes:
        #initial_route = route["instruction"]
        initial_route = " ".join(route["instruction"].split()[:4])
        generated = ''
        line = ''

        start_index = randint(0, len(text)-maxlen-1)

        while len(initial_route) < maxlen:
            initial_route = initial_route + " " + text[start_index:start_index+maxlen]
        if len(initial_route) > maxlen:
            initial_route = initial_route[:maxlen]

        sentence = initial_route

        for i in range(length):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.
            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]
            generated += next_char
            sentence = sentence[1:] + next_char

            line = ' '.join(initial_route.split()[:3]) + ' ' +' '.join(generated[40:].split())

        doc = nlp(line)
        nouns = [item.text for item in doc if item.pos_ == 'NOUN']
        adjs = [item.text for item in doc if item.pos_ == 'ADJ']
        line = line.partition(choice(nouns))[0] + choice(nouns) + '.'
        line = " ".join(line.split()).capitalize()
        #generated = ' '.join(initial_route.split()[:2]) + " " + generated
        instructions.append(line)
    return jsonify(status='success', result=instructions);



# markov version
@app.route('/_markov')
def markovme():
    instructions = []
    routes = json.loads(request.args['routes'])

    for route in routes:
        seed = route["instruction"].split()[:2]
        line = " ".join(markov.generate(markov_model, 2, seed))
        instructions.append(line)
    return jsonify(status='success', result=instructions);

# Run the server
if __name__ == "__main__":
    app.run()
    #app.run( host='0.0.0.0', port=8080, debug=False )
