# Author: Jeremi Torój
# Date: 27/05/2024

from flask import Flask, request, jsonify, render_template
from parser import process_file


ALLOWED_EXTENSIONS = {'txt', 'csv', 'json'}

app = Flask(__name__)

# @app.route('/metrics')
# def metrics():


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        summary = process_file(file)
        return jsonify(summary), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
