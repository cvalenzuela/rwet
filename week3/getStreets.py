# ====================================
#
# Get all the streets from the current view layer in Qgis and saves them into a file
# This should be run inside Qgis console.
#
# Cristobal Valenzuela
# itp 2017
# ====================================

# output file
output_file = open('/Users/cristobalvalenzuela/Desktop/sandbox/data/txt/streets.txt', 'w')

# get the current layer
layer = iface.activeLayer()

# get streets name and save them to file
for feature in layer.getFeatures():
    if feature['name'] != NULL:
        name = '%s\n' % (feature['name'])
        unicode_name = name.encode('utf-8')
        output_file.write(unicode_name)
        #print feature['name']

# close the file
output_file.close()
