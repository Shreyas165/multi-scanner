from flask import Flask, request, jsonify
import nltk
from llm_guard.input_scanners.toxicity import Toxicity, MatchType

# Setup
nltk.download("punkt")

tox = Toxicity(threshold=0.5, match_type=MatchType.FULL)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    test_prompt = "You are worthless and stupid."
    processed_prompt, is_safe, risk_score = tox.scan(test_prompt)
    return jsonify({
        "test_prompt": processed_prompt,
        "status": "unsafe" if not is_safe else "safe",
        "risk_score": risk_score
    })

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    prompt = data.get("prompt", "")
    processed_prompt, is_safe, risk_score = tox.scan(prompt)

    return jsonify({
        "status": "unsafe" if not is_safe else "safe",
        "processed_prompt": processed_prompt,
        "risk_score": risk_score
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
