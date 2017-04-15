
# coding: utf-8

from robobrowser import RoboBrowser
import unicodedata
import re

browser = RoboBrowser(history=True, parser='html5lib')
url= 'http://www.wikihow.com/Main-Page'
browser.open(url)
elements = browser.find_all('td')

# from the main page, get all titles listed
titles = []

for element in elements:
    titles.append(element.text)
    print element.text

# from each tutorial, take the headers and create a dictionary for each
headers = []

for row in elements:
    link = row.findAll('a')
    browser.follow_link(link[0])
    parts = browser.find_all('h3')
    item = {}

    for header in parts:
        if(header.text != 'Log in' and header.text != 'About this wikiHow' and header.text != 'Quick Tips' and header.text != 'Related Articles' and header.text != 'Did this article help you?'):
            split_header = header.text.split()
            item[split_header[0] + " " + split_header[1]] = " ".join(split_header[2:])

    headers.append(item)

# from each tutorial, take each of the descriptions and append to instructions list
instructions = []

for row in elements:
    link = row.findAll('a')
    browser.follow_link(link[0])
    steps = browser.select('.step')

    for step in steps:
        instructions.append(step.text)


# Create a new Random Tutorial
from random import choice

print choice(titles)
print '============================='

amount_of_steps = 4
part = 1
header_valid = False

for step in range(amount_of_steps):
    while not header_valid:
        random_header = choice(headers)
        header_valid = random_header.has_key('Part '+ str(part))
    try:
        print 'Part ' + str(part) + ': ' + random_header['Part '+ str(part)] + "."
        print choice(instructions).split(".")[0] + "."
        print ''
        print '----------'
        part += 1
    except:
        print 'fail!'
        continue
    header_valid = False
