# coding: utf-8

import sys
import codecs
import pronouncing
import nltk
import re
import glob
import json
from random import choice
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

# helper functions from nltk
nltk.download("punkt")
nltk.download("stopwords")
tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")

# Source files

# bash docs
bash_docs = open('data/bash.txt').read()

# python docs
python_docs = sorted(glob.glob('data/python-2.7.13-docs-text/tutorial/*.txt'))
python_raw = u""
# read every file and append it to corpus raw
for element in python_docs:
    with codecs.open(element,"r","utf-8") as element_file:
        python_raw += element_file.read()

# ulyses
ulyses = strip_headers(load_etext(4300)).strip()

# replacers (not used for now)
occupations = open('data/occupations.json').read()
occupations = json.loads(occupations)

# js docs
js_docs = open('data/jsdocs.txt').read().decode('ascii', errors="replace")

# Assembly docs
assembly_docs = open('data/assembler-guide.txt').read().decode('ascii', errors="replace")

# the list of words to use
all_words = assembly_docs.split()

# functions to create
def create_line(position):
    temp_index = position
    sentence = ''
    while len(sentence.encode('utf-8')) < 32:
        word = all_words[temp_index]
        sentence = sentence + " " +  word
        temp_index -= 1

    sentence32 = []
    for word in sentence.split():
        clean_word = word.replace(".", "")
        clean_word = clean_word.replace(" ", "")
        clean_word = clean_word.replace(",", "")
        clean_word = clean_word.lower()
        sentence32.append(clean_word)

    return " ".join(reversed(sentence32))
    #words = all_words[position-5 : position+1]
    #line = []
    #for word in words:
        #clean_word = word.replace(".", "")
        #line.append(clean_word)
   # return " ".join(line)

def two_sentences():
    x1 = ''
    x2 = ''
    sentences = []
    while len(x2) == 0:
        x1_word = choice(all_words)
        try:
            x2_word = choice(pronouncing.rhymes(x1_word))
        except:
            x2_word = ''
        if len(x2_word) > 0:
            x1_index = all_words.index(x1_word)
            try:
                x2_index = all_words.index(x2_word)
            except:
                x2_index = 0
            if x2_index != 0:
                x1 = create_line(x1_index)
                x2 = create_line(x2_index)
                sentences.append(x1)
                sentences.append(x2)
    return sentences



# An original sonnet is 14 lines, each being 10 syllables long.
# The structure is: ab ab, cdcd, efef, gg

# A bit sonnet is 2^4 lines, each being an average of 2^5 syllables long.
# The structure is: aa, bb cc, dede, ff, gg
# The corpus can only be programming documentation

a = two_sentences()
b = two_sentences()
c = two_sentences()
d = two_sentences()
e = two_sentences()
f = two_sentences()
g = two_sentences()

print a[0]
print a[1]

print b[0]
print b[1]

print c[0]
print c[1]

print d[0]
print e[1]
print d[0]
print e[1]

print f[0]
print f[1]

print g[0]
print g[1]
