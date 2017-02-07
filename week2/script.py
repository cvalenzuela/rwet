# ====================================
# Assignment #2 RWET
#
# This script takes cooking recepies and replace random nouns with 
# nouns found in a Tax/IRS Dictionary (https://www.taxact.com/tax-terms/tax-dictionary.asp)
#
# Cristobal Valenzuela
# itp 2017
# ====================================

from textblob import TextBlob
from random import randint
import sys

# Open the files
fileOne = TextBlob(open("recepies.txt").read().decode('ascii', errors="replace"))
fileTwo = TextBlob(open("irs.txt").read().decode('ascii', errors="replace"))

# Get all the nouns from the recepies text
nounsFileOne = fileOne.noun_phrases

# Get all the nouns from the irs file
nounsFileTwo = fileTwo.noun_phrases

# For each line in the recepies file, change a random noun using one from the irs file
for line in fileOne.sentences:
    if len(line.noun_phrases):
        randomNounOriginal = randint(0,len(line.noun_phrases)-1)
        randomNounReplace = randint(0,len(nounsFileTwo)-1)
        print line.replace(line.noun_phrases[randomNounOriginal], nounsFileTwo[randomNounReplace])
