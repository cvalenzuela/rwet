#!/usr/bin/python
movie_quotes = open("data/moviequotes.memorable_quotes.txt").read().split('\n')

movie_quotes[102]
lines = []

for line in movie_quotes:
    line = line.strip()
    if len(line) > 2:
        line = unicode(line, errors='replace')
        lines.append(line)
