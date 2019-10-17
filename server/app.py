from flask import Flask, jsonify
from flask_cors import CORS
from flask import abort, redirect, url_for, render_template
from flask import request, session
import json

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/results', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    resList = []
    if request.method == 'POST':
        post_data = request.get_json()
        resList.append({
            'title': post_data.get('title'),
            'link': post_data.get('link'),
            'content': post_data.get('content')
        })
    response_object['data'] = resList
    return jsonify(response_object)

@app.route('/', methods=['GET'])
def index():
    return jsonify('main page')


if __name__ == '__main__':
    app.run()