from flask import Flask, request, jsonify
import jwt
import hmac
import hashlib
import base64

app = Flask(__name__)

# Load the keys
with open('keys/private.pem', 'rb') as f: PRIVATE_KEY = f.read()
with open('keys/public.pem', 'rb') as f: PUBLIC_KEY = f.read()

@app.route('/public.pem', methods=['GET'])
def get_pub(): 
    return PUBLIC_KEY, 200, {'Content-Type': 'text/plain'}

@app.route('/', methods=['GET'])
def index():
    token = jwt.encode({"user": "guest", "role": "guest"}, PRIVATE_KEY, algorithm="RS256")
    # Handle the string/bytes discrepancy depending on the PyJWT version running
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return jsonify({"message": "Writeup-DB Node 05. Extract public key at /public.pem", "token": token})

@app.route('/admin', methods=['GET'])
def admin():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token: return jsonify({"error": "Missing token"}), 401

    try:
        # Step 1: Read the unverified header to check the algorithm
        header = jwt.get_unverified_header(token)
        alg = header.get('alg', '')

        # VULNERABILITY: The Algorithm Confusion Implementation
        if alg == 'HS256':
            # The server mistakenly allows HS256 and manually verifies it 
            # using the PUBLIC_KEY string as the HMAC password.
            parts = token.split('.')
            if len(parts) != 3: 
                raise Exception("Invalid JWT format")

            message = f"{parts[0]}.{parts[1]}".encode()
            signature = parts[2]

            # Calculate what the HMAC signature *should* be using the Public Key
            expected_sig = base64.urlsafe_b64encode(
                hmac.new(PUBLIC_KEY, message, hashlib.sha256).digest()
            ).decode().rstrip("=")

            if hmac.compare_digest(signature, expected_sig):
                decoded = jwt.decode(token, options={"verify_signature": False})
            else:
                raise Exception("HMAC verification failed.")
                
        elif alg == 'RS256':
            decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        else:
            raise Exception("Unsupported Algorithm")

        # Grant access if the payload claims admin
        if decoded.get("role") == "admin":
             return jsonify({"flag": "FLAG{4symm3tr1c_c0nfus10n_succ3ss}"})
        return jsonify({"message": "Access Denied. Guest clearance."}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 400