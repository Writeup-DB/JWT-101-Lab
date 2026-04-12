from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
# VULNERABILITY: Weak, crackable secret
WEAK_SECRET = "shadow" 

@app.route('/', methods=['GET'])
def index():
    token = jwt.encode({"user": "guest", "role": "guest"}, WEAK_SECRET, algorithm="HS256")
    return jsonify({"message": "Writeup-DB Node 02.", "token": token})

@app.route('/admin', methods=['GET'])
def admin():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token: return jsonify({"error": "Missing token"}), 401

    try:
        decoded = jwt.decode(token, WEAK_SECRET, algorithms=["HS256"])
        if decoded.get("role") == "admin":
            return jsonify({"flag": "FLAG{sh4d0ws_c4nn0t_h1d3_y0u}"})
        return jsonify({"message": "Access Denied: Guest clearance."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400