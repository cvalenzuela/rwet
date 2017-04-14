#!/usr/bin/python
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory, render_template
from random import choice, sample
from corpus import lines

# set up flask app
app = Flask(__name__)
app.debug = True

# Routes
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/_get_text')
def add_numbers():
    lat = request.args['lat']
    lng = request.args['lng']
    length = request.args['length']
    # check conditional of th length maybe?
    # a = request.args.get('a', 0, type=int)
    # b = request.args.get('b', 0, type=int)
    # return jsonify(result=a + b)
    return jsonify(result = sample(lines, int(length)))
    # maybe this too? = return jsonify({'response': output})

if __name__ == "__main__":
    app.run()
