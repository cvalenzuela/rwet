#!/usr/bin/python
from flask import Flask, jsonify, request, render_template
import markov
import json

# set up flask app
app = Flask(__name__, static_url_path='')
app.debug = False

#metamorphosis, shakespear , gutenberg, darwin
text = open('source_text/gutenberg.txt').read().lower()
text = text.split()
model = markov.build_model(text, 1)

# Main Route
@app.route("/")
def index():
    return render_template('index.html')

# markov version
@app.route('/_markov')
def markovme():
    instructions = []
    routes = json.loads(request.args['routes'])
    for route in routes:
        seed = route["instruction"].split()[:1]
        line = " ".join(markov.generate(model, 1, seed))
        while(len(line) > 100):
            line = " ".join(markov.generate(model, 1, seed))
            line = line.partition(".")[0].capitalize() + '.'
        instructions.append(line)
    return jsonify(status='success', result=instructions);

# Run the server
if __name__ == "__main__":
    app.run()
    #app.run( host='0.0.0.0', port=8080, debug=False )
