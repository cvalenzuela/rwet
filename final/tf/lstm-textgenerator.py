# coding: utf-8

# high level wrapper for tensorflow
import keras
from keras.models import Sequential # series of layers
from keras.layers import LSTM # lstm
from keras.layers import Dense, Activation # fully connected network
from keras.utils.data_utils import get_file # helper function to download from the internet
from keras.optimizers import RMSprop # gradient descent to run more efficiently
import numpy as np
import random
import sys

from utils import sample # the name of the function in the utils

# Step 1 - get your data
#path = get_file('nietzche.txt', origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
path = 'edgarallanpoe.txt'

text = open(path, encoding="utf8").read().lower() # read the file and convert it to lowercase

# get and sort all unique characters
chars = sorted(list(set(text)))

# what position does each character exist at in the prev list. create a dictionary for it. two in reverse
char_indices = dict((c,i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut your text into overlapping sequences
maxlen = 40
sentences = []
next_chars = []

for i in range(0, len(text)-maxlen, 3):
    sentences.append(text[i:i+maxlen])
    next_chars.append(text[i+maxlen])

# vectorization
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y =np.zeros((len(sentences), len(chars)), dtype=np.bool)

# vector representation of a sentence
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# build LSTM model
# 2MB 256 or 128
# 5-8MB 512
# 10-20MB 1024
# 25+
model = Sequential()
model.add(LSTM(512, input_shape=(maxlen, len(chars))))
#model.add(LSTM(512, _____))
#model.add(LSTM(512, _____))
model.add(Dense(len(chars))) # fully connected nn
model.add(Activation('softmax'))
optimizer = RMSprop(lr=0.001) # perform gradient descent
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

# train your model
for iteration in range(1,2):
    print('Iteration', iteration)
    model.fit(X, y, batch_size=128, epochs=10) # epochs is looping over the sentence in batches of 128

    start_index = random.randint(0, len(text)-maxlen-1)

    for diversity in [0.2, 0.5, 1.0, 1.2]: # how free is going to be in the predicions also called temperature
        generated = ''
        sentence = text[start_index:start_index+maxlen] # randomly picking 40 chars for my seed
        generated += sentence
        print("My seed is", sentence)
        sys.stdout.write(generated)

        for i in range(400):
            x = np.zeros((1, maxlen, len(chars)))
            for t,char in enumerate(sentence):
                x[0,t,char_indices[char]] = 1

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char
            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()
    model.save("edgarallanpoe.h5")

# import keras
# from keras.models import load_model
# model = load_model(filename)
