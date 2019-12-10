from flask import Flask, jsonify
from flask_cors import CORS
from flask import abort, redirect, url_for, render_template
from flask import request, session
import json
import search_engine

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
    
@app.route('/query', methods=['GET', 'POST'])
def search():
    parser = search_engine.Parser()
    searcher = search_engine.Searcher(index_path = './indexdir', parser = parser)
    query = request.form.get('query', 'information retrieval')
    results = searcher.search(query)
    return jsonify(results)

@app.route('/relevance', methods=['GET', 'POST'])
def relevance():
    title = request.form.get('title')
    path =  request.form.get('path')
    relevant = request.form.get('relevant')
    # do something to log the relevance

    res = {'title':title, 'relevant':relevant}
    return jsonify(res)

@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    parser = search_engine.Parser()
    searcher = search_engine.Searcher(index_path = './indexdir', parser = parser)
    query = request.form.get('query', 'information retrieval')
    results = searcher.suggest(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run()
