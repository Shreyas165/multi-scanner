from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Scanner API is runninggg."

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    return jsonify({
        "status": "success",
        "scanner": "2",
        "result": f"Processed: {data}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)