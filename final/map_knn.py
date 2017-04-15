# -*- coding: utf-8 -*-
# create a map with the data
# find the knn for each data point

from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd

# load the knn model
td = pd.read_csv("data/traffic_deaths.csv", dtype=str)

geodata = pd.concat([td['streetview_latitude'], td['streetview_longitude'], td['description'] ] , axis=1, keys=['lat', 'lng', 'description'])
latlng = geodata[['lat','lng']].values.tolist()

neigh = NearestNeighbors(n_neighbors=1, algorithm='ball_tree', radius=2.0)
neigh.fit(latlng)

# get knn for given lat lng
def get_knn(lat, lng, instruction):
    # find the 1-knn for a given point
    knn = neigh.kneighbors([[lat, lng]], 1, return_distance=False)[0][0]
    instruction = ' '.join(instruction.split()[:2]) + " and " + geodata.iloc[[knn]]['description'][knn]
    return instruction

    # Create a map (debug in jupyter)
    # import folium
    # map = folium.Map(location=[40.738584, -73.810767], zoom_start=10, tiles='Stamen Toner')
    # for index, row in traffic_deaths.iterrows():
    #     lat = row['streetview_latitude']
    #     lng = row['streetview_longitude']
    #     map.add_children(folium.CircleMarker([lat,lng],color='rgba(255,0,0,0.75)',fill_color='rgba(255,0,0,0.75)', radius=200))
