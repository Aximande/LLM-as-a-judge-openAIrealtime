# router.py
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Streamlit

@app.route('/start-session', methods=['POST'])
def start_session():
    return jsonify({
        "status": "success",
        "message": "Session started",
        "participants": [
            {"name": "Judge Penney Azcarate", "role": "Judge", "status": "speaking"},
            {"name": "Ben Chew", "role": "Depp's Attorney", "status": "waiting"},
            {"name": "Ben Rottenborn", "role": "Heard's Attorney", "status": "waiting"}
        ]
    })

@app.route('/next-dialogue', methods=['GET'])
def next_dialogue():
    return jsonify({
        "speaker": "Judge Penney Azcarate",
        "text": "The court is now in session.",
        "timestamp": "10:00 AM"
    })

@app.route('/action', methods=['POST'])
def handle_action():
    action = request.json.get('action')
    return jsonify({
        "status": "success",
        "action": action,
        "result": f"Action {action} processed"
    })

if __name__ == '__main__':
    app.run(debug=True)