from flask import Flask, request, jsonify
import jwt
import os

app = Flask(__name__)
KEY_DIR = "./keys/"

@app.route('/', methods=['GET'])
def index():
    token = jwt.encode({"user": "guest", "role": "guest"}, "dummy_secret", algorithm="HS256", headers={"kid": "secret_key1.pem"})
    return jsonify({"message": "Writeup-DB Node 03.", "token": token})

@app.route('/admin', methods=['GET'])
def admin():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token: return jsonify({"error": "Missing token"}), 401

    try:
        kid = jwt.get_unverified_header(token).get('kid')
        key_path = os.path.join(KEY_DIR, str(kid))
        
        try:
            with open(key_path, 'r') as f:
                secret = f.read().strip()
        except FileNotFoundError:
            return jsonify({"error": "Key not found in databanks"}), 500

        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        if decoded.get("role") == "admin":
             return jsonify({"flag": "FLAG{p4th_tr4v3rs4l_4ch13v3d}"})
        return jsonify({"message": "Access Denied: Guest clearance."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400