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
    
@app.route('/query', methods=['POST'])
def search():
    parser = search_engine.Parser()
    searcher = search_engine.Searcher(index_path = './indexdir', parser = parser)
    query = request.form.get('query', 'information retrieval')
    results = searcher.search(query)
    return jsonify(results)


if __name__ == '__main__':
    app.run()
