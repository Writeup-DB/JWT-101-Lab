from flask import Flask, request, jsonify
import jwt
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Provide a baseline token to populate the UI.
    # The dummy 'jku' header hints at the internal architecture.
    headers = {
        "jku": "http://internal-auth.writeup-db.local/.well-known/jwks.json",
        "kid": "core-key-01"
    }
    payload = {"user": "guest", "role": "guest"}
    
    # We sign it with a dummy symmetric key just to generate a valid JWT string.
    # (The admin endpoint will expect your forged RS256 signature anyway).
    token = jwt.encode(payload, "dummy_secret", algorithm="HS256", headers=headers)
    
    # Handle the string/bytes discrepancy just in case PyJWT versions differ
    if isinstance(token, bytes):
        token = token.decode('utf-8')
        
    return jsonify({
        "message": "Writeup-DB Node 06. Intercepted baseline telemetry.", 
        "token": token
    })

@app.route('/admin', methods=['GET'])
def admin():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token: return jsonify({"error": "Missing token"}), 401

    try:
        unverified_headers = jwt.get_unverified_header(token)
        jku_url = unverified_headers.get('jku')
        
        if not jku_url: return jsonify({"error": "JKU header missing"}), 400

        # VULNERABILITY: Blindly fetching from attacker-controlled URL
        jwks = requests.get(jku_url, timeout=3).json()
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwks['keys'][0]))

        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        if decoded.get("role") == "admin":
             return jsonify({"flag": "FLAG{r3m0t3_k3y_h1j4ck_c0mpl3t3}"})
        return jsonify({"message": "Access Denied."}), 403
    except Exception as e:
        return jsonify({"error": f"Validation failed: {str(e)}"}), 400