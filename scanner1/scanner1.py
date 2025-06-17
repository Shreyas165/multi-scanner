from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Scanner API is running."

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    return jsonify({
        "status": "success",
        "scanner": "1",
        "result": f"Processed: {data}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
