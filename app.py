"""Small, stateless Flask application for a local Docker learning lab."""
from flask import Flask, jsonify

app = Flask(__name__)


@app.get('/')
def index():
    return jsonify(service='docker-github-lab', message='Hello from Docker & GitHub Lab!')


@app.get('/health')
def health():
    return jsonify(status='ok'), 200
