import os
from flask import Flask, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Load once at startup (super fast on Railway)
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

@app.route("/")
def home():
    return jsonify({"status": "✅ Czech & Slovak Namedays + Holidays API running (self-hosted on Railway)"})

@app.route("/today")
def today():
    today_date = datetime.now().strftime("%m-%d")
    
    return jsonify({
        "date": today_date,
        "czech_nameday": data["namedays_czech"].get(today_date, "—"),
        "slovak_nameday": data["namedays_slovak"].get(today_date, "—"),
        "czech_holidays": [
            h for h in data.get("holidays_czech", [])
            if h["date"] == today_date
        ],
        "slovak_holidays": [
            h for h in data.get("holidays_slovak", [])
            if h["date"] == today_date
        ]
    })

@app.route("/date/<date>")
def get_date(date):
    # Accept both MM-DD and YYYY-MM-DD
    if len(date) == 10:
        date = date[5:]          # strip year
    elif len(date) != 5:
        return jsonify({"error": "Use MM-DD or YYYY-MM-DD"}), 400

    return jsonify({
        "date": date,
        "czech_nameday": data["namedays_czech"].get(date, "—"),
        "slovak_nameday": data["namedays_slovak"].get(date, "—"),
        "czech_holidays": [h for h in data.get("holidays_czech", []) if h["date"] == date],
        "slovak_holidays": [h for h in data.get("holidays_slovak", []) if h["date"] == date]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)