from flask import Flask, request, jsonify
import jwt, requests, json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Writeup-DB Node 06. Awaiting remote JWKS telemetry."})

@app.route('/admin', methods=['GET'])
def admin():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token: return jsonify({"error": "Missing token"}), 401

    try:
        jku_url = jwt.get_unverified_header(token).get('jku')
        if not jku_url: return jsonify({"error": "JKU header missing"}), 400

        # VULNERABILITY: Blindly fetching from attacker-controlled URL
        jwks = requests.get(jku_url, timeout=3).json()
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwks['keys'][0]))

        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        if decoded.get("role") == "admin":
             return jsonify({"flag": "FLAG{r3m0t3_k3y_h1j4ck_c0mpl3t3}"})
        return jsonify({"message": "Access Denied."}), 403
    except Exception as e:
        return jsonify({"error": "Validation failed."}), 400