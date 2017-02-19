# ====================================
# Assignment #3 RWET
#
# Using the map of New York City, this script changes the names of the streets with random lines from the movie script **"Salò, or the 120 Days of Sodom"** by Pier Paolo Pasolini's
#
# Cristobal Valenzuela
# itp 2017
# ====================================


# files
salo_cleaned = open("data/txt/salo_cleaned.txt", "r+")

# get rid of spaces and lines in original script
with open("salo.txt", "r") as file:
    for line in file:
        cleanedLine = line.strip()
        if cleanedLine:
            cleanedLine = line.strip(".")
            cleanedLine = line.lstrip()
            salo_cleaned.write(cleanedLine)

# close all files
salo_cleaned.close()
