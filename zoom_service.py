import requests
import jwt
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = 'your_zoom_api_key'
API_SECRET = 'your_zoom_api_secret'

# not sure if using..... leave it first 

def generate_jwt():
    payload = {
        'iss': API_KEY,
        'exp': int(time.time()) + 5000
    }
    token = jwt.encode(payload, API_SECRET, algorithm='HS256')
    return token

@app.route('/zoom/create_meeting', methods=['POST'])
def create_zoom_meeting():
    data = request.get_json()
    topic = data.get("topic", "Consultation")
    start_time = data.get("start_time")  # ISO format
    duration = data.get("duration", 30)

    headers = {
        'Authorization': f'Bearer {generate_jwt()}',
        'Content-Type': 'application/json'
    }

    payload = {
        "topic": topic,
        "type": 2,
        "start_time": start_time,
        "duration": duration,
        "timezone": "Asia/Singapore",
        "settings": {
            "join_before_host": True,
            "approval_type": 0,
            "audio": "voip",
            "auto_recording": "cloud"
        }
    }

    response = requests.post("https://api.zoom.us/v2/users/me/meetings", headers=headers, json=payload)
    return jsonify(response.json()), response.status_code
