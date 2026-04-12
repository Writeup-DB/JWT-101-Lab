from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET = "core_system_override"

@app.route('/', methods=['GET'])
def index():
    token = jwt.encode({"user": "guest", "role": "guest"}, SECRET, algorithm="HS256")
    return jsonify({"message": "Writeup-DB Node 01.", "token": token})

@app.route('/admin', methods=['GET'])
def admin():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token: return jsonify({"error": "Missing token"}), 401

    try:
        unverified = jwt.get_unverified_header(token)
        if unverified.get('alg', '').lower() == 'none':
            decoded = jwt.decode(token, options={"verify_signature": False})
        else:
            decoded = jwt.decode(token, SECRET, algorithms=["HS256"])

        if decoded.get("role") == "admin":
            return jsonify({"flag": "FLAG{w3lc0m3_t0_th3_n0n3_m41nfr4m3}"})
        return jsonify({"message": "Access Denied: Guest clearance."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400