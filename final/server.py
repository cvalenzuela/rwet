#!/usr/bin/python

from flask import Flask, jsonify, request, redirect, url_for, send_from_directory, render_template
from random import choice, sample
from instructions import generate_instructions
import json

import keras
from keras.models import load_model
import numpy as np

# set up flask app
app = Flask(__name__)
app.debug = False

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

model = load_model('model.h5')

maxlen = 40
text = open('hamlet.txt').read().lower()  # read the file and convert to lowercase
chars = sorted(list(set(text)))
# what position does each character exist at in the prev list
char_indices = dict((c,i) for i, c in enumerate(chars))
indices_char = dict((i,c) for i,c in enumerate(chars))

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
    #sentence = 'ince of denmark hamlet prince of denmark'
    diversity = float(0.4)
    length = int(97)

    for route in routes:
        sentence = 'ince of denmark hamlet prince of denmark'
        initial_route = route["instruction"]
        generated = ''
        # generated += sentence
        for i in range(length):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.
            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]
            generated += next_char
            sentence = sentence[1:] + next_char
        generated = ' '.join(initial_route.split()[:2]) + generated
        instructions.append(generated)
    return jsonify(status='success', result=instructions);

# Run the server
if __name__ == "__main__":
    app.run()
