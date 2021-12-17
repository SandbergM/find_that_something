from search_engine.Searcher import Searcher
import cv2


from flask import Flask, request
from flask_cors import CORS
import json
from flask import jsonify

app = Flask(__name__)

CORS(app)

image_searcher = Searcher()

@app.route('/search', methods=['POST'])
def search():
    res = image_searcher.search(request.data)
    return jsonify(res), 200




if __name__ == '__main__':
    app.run( port=5000 )