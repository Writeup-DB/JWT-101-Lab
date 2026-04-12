from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

with open('keys/private.pem', 'rb') as f: PRIVATE_KEY = f.read()
with open('keys/public.pem', 'rb') as f: PUBLIC_KEY = f.read()

@app.route('/public.pem', methods=['GET'])
def get_pub(): return PUBLIC_KEY, 200, {'Content-Type': 'text/plain'}

@app.route('/', methods=['GET'])
def index():
    token = jwt.encode({"user": "guest", "role": "guest"}, PRIVATE_KEY, algorithm="RS256")
    return jsonify({"message": "Writeup-DB Node 05. Extract public key at /public.pem", "token": token})

@app.route('/admin', methods=['GET'])
def admin():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token: return jsonify({"error": "Missing token"}), 401

    try:
        # VULNERABILITY: Allowing both asymmetric and symmetric algs with the public key
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256", "HS256"])
        if decoded.get("role") == "admin":
             return jsonify({"flag": "FLAG{4symm3tr1c_c0nfus10n_succ3ss}"})
        return jsonify({"message": "Access Denied."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400