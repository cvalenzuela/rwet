# ====================================
#
# Change the streets name for a random line in the given file
# This should be run inside Qgis console.
#
# Cristobal Valenzuela
# itp 2017
# ====================================

from random import randint

# script file
script = open('/Users/cristobalvalenzuela/Dropbox/itp/spring2017/reading_and_writting/work/week3/data/txt/salo_cleaned.txt', 'r+')

# get the current layer
layer = iface.activeLayer()

# enable edit in layer
layer.startEditing()

# push all the lines into a list
script_lines = []
for line in script:
    script_lines.append(line)

# Change all the streets name
for feature in layer.getFeatures():
    if feature['name'] != NULL:
        random_line = randint(0, len(script_lines)-1)
        feature['name'] = script_lines[random_line]
        layer.updateFeature(feature)

# commit the changes to the layer
layer.commitChanges()

# close the file
script.close()
