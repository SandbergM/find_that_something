from search_engine.Searcher import Searcher
from flask import send_file
import os
from flask import Flask, request
from flask_cors import CORS
import json
from flask import jsonify
import cv2

app = Flask(__name__)

CORS(app)

image_searcher = Searcher()

@app.route('/search', methods=['POST'])
def search():
    res = image_searcher.search(request.data)
    return jsonify(res), 200

@app.route('/image', methods=["GET"])
def send_image():
    status_code, img_path = image_searcher.send_image(request.args.get("image_id"))
    return send_file(f'{os.path.dirname(__file__)}/{img_path}', mimetype='image/jpg'), status_code

@app.route('/image', methods=["post"])
def add_image():
    image_searcher.append_data(request.data)
    return "Image added", 201

@app.route('/reset', methods=["GET"])
def reset_dataset():
    image_searcher.reset_dataset()
    return "Done!", 200

if __name__ == '__main__':
    app.run( port=5000 )