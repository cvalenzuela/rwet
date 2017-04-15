#!/usr/bin/python
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory, render_template
from random import choice, sample
from instructions import generate_instructions
import json

# set up flask app
app = Flask(__name__)
app.debug = True

# Main Route
@app.route("/")
def index():
    return render_template('index.html')

# Generate Text route
@app.route('/_get_text')
def add_numbers():
    routes = json.loads(request.args['routes'])
    text = generate_instructions(routes)
    return jsonify(result = text)

# Run the server
if __name__ == "__main__":
    app.run()
