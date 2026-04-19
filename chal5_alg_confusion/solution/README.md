## Node 05: The Doppelgänger (Algorithm Confusion)
The server expects RS256 (Asymmetric) but will blindly process HS256 (Symmetric) using the public key as the shared secret.

1. Fetch the Public Key: Make a GET request to `http://localhost/api/chal5/public.pem` and save the exact text of the key.
2. Modify the Token: Decode your initial token. Change the header: `"alg": "HS256"`. Change the payload: `"role": "admin"`.
3. Sign with the Public Key: Go to jwt.io. Paste your modified header and payload. In the "Verify Signature" section, paste the exact contents of the `public.pem` file (including the `-----BEGIN PUBLIC KEY-----` and `-----END PUBLIC KEY-----` lines and all newlines).
4. Submit: The server will grab its public key, see you used `HS256`, and use that public key string as a symmetric HMAC password to validate your forged token.


### Note - It will not work by default
The application is using PyJWT==2.8.0. Modern versions of the PyJWT library explicitly check for the Algorithm Confusion vulnerability (CVE-2015-9256). When the library sees an asymmetric key (like your RSA public key starting with -----BEGIN PUBLIC KEY-----) being passed alongside a symmetric algorithm (HS256), it hard-blocks the operation and throws the exact error you received.

If you wanna make this challenge work make modificaitons.
Step 1: Modify the Requirements (requirements.txt)
```plaintext
Flask==3.0.3
gunicorn==22.0.0
PyJWT==1.7.1 #Changed
requests==2.31.0
cryptography==42.0.5
```

Step 2: Update the Application Code
- PyJWT 1.7.1 handles decoding slightly differently than 2.x. You need to remove the algorithms list restriction in the jwt.decode function so it accepts whatever algorithm the token dictates.
- Open chal5_alg_confusion/app.py and update the vulnerable line:
```pyhton
# CHANGE THIS (Version 2.8.0 syntax):
# decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256", "HS256"])

# TO THIS (Version 1.7.1 syntax):
decoded = jwt.decode(token, PUBLIC_KEY)
```

Step 3: Rebuild the Node
Because you changed the requirements.txt, you must rebuild the Docker container for the changes to take effect. Run the following commands from your master repo directory:
```bash
docker-compose stop chal5_alg_confusion
docker-compose build chal5_alg_confusion
docker-compose up -d chal5_alg_confusion
```
Once the container is back online, your exact same HTTP request will bypass the library's checks, use the public key as the HMAC secret, and yield the flag.