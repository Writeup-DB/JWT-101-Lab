from flask import Flask, request, jsonify
import hmac, hashlib, base64, json

app = Flask(__name__)
ADMIN_SEC = "complex_admin_key_999"
GUEST_SEC = "guest"

def b64d(s): return base64.urlsafe_b64decode(s + '=' * (4 - len(s) % 4))

@app.route('/', methods=['GET'])
def index():
    hdr = base64.urlsafe_b64encode(b'{"alg":"HS256"}').decode().rstrip("=")
    pyl = base64.urlsafe_b64encode(b'{"user":"student","role":"guest"}').decode().rstrip("=")
    sig = base64.urlsafe_b64encode(hmac.new(GUEST_SEC.encode(), f"{hdr}.{pyl}".encode(), hashlib.sha256).digest()).decode().rstrip("=")
    return jsonify({"message": "Writeup-DB Node 04.", "token": {"payload": pyl, "signatures": [{"protected": hdr, "signature": sig}]}})

@app.route('/admin', methods=['POST'])
def admin():
    data = request.json
    try:
        pyl_b64 = data['payload']
        decoded_pyl = json.loads(b64d(pyl_b64).decode())
        is_valid = False

        for sig_block in data['signatures']:
            sig_input = f"{sig_block.get('protected', '')}.{pyl_b64}".encode()
            for sec in [ADMIN_SEC, GUEST_SEC]:
                exp_sig = base64.urlsafe_b64encode(hmac.new(sec.encode(), sig_input, hashlib.sha256).digest()).decode().rstrip("=")
                if hmac.compare_digest(sig_block.get('signature', ''), exp_sig):
                    is_valid = True
                    break
            if is_valid: break

        if is_valid and decoded_pyl.get("role") == "admin":
             return jsonify({"flag": "FLAG{mult1_s1g_n3tw0rk_c0mpr0m1s3d}"})
        return jsonify({"message": "Access Denied: Invalid parameters."}), 401
    except Exception:
        return jsonify({"error": "Malformed JWS JSON"}), 400