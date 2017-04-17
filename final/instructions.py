# -*- coding: utf-8 -*-
import json
import pandas
from map_knn import get_knn

# test query
#routes = json.loads(open("data/querysample.json").read())
# for every instruction, get the first two words
# for i in range(len(query)):
#     instructions.append(query[i]['instruction'].split()[:2])
#     print query[i]['instruction']

# generate the instructions for the received route
def generate_instructions(routes):
    instructions = []
    for instruction in routes:
        instructions.append(get_knn(instruction["lat"], instruction["lng"], instruction["instruction"]))
    return instructions
