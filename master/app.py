from flask import Flask, request, jsonify
from psycopg2.extras import Json
import requests
import psycopg2

app = Flask(__name__)

# Scanner endpoints (will be resolved by Docker/K8s DNS)
SCANNER1_URL = "http://scanner1-service:5001/scan"
SCANNER2_URL = "http://scanner2-service:5002/scan"

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="db-service",
        database="scandb",
        user="postgres",
        password="password"
    )
    return conn

@app.route('/', methods=['GET'])
def home():
    return "Master service running!"


@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    
    try:
        # Send to Scanner 1
        response1 = requests.post(SCANNER1_URL, json=data).json()
        store_scan("scanner1", response1)
        
        # Send to Scanner 2
        response2 = requests.post(SCANNER2_URL, json=data).json()
        store_scan("scanner2", response2)
        
        return jsonify({
            "scanner1": response1,
            "scanner2": response2,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def store_scan(scanner_id, scan_data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scans (scanner, data) VALUES (%s, %s)",
        (scanner_id, Json(scan_data))
    )
    conn.commit()
    cur.close()
    conn.close()


