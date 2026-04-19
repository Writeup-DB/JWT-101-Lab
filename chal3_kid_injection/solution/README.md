## Node 03: The Ghost in the Path (kid Injection)
The server blindly uses the Key ID (kid) to read files from the local disk to use as the verification secret.

1. Obtain the Token: Get the initial token.
2. Path Traversal in Header: Decode the token and modify the header to traverse directories and point to a known empty file in Linux systems.
```JSON
{
  "alg": "HS256",
  "kid": "../../../../../../dev/null"
}
```

3. Elevate Payload: Change `"role": "guest"` to `"role": "admin"`.
4. Sign with a Void: Because /dev/null is empty, the server will read an empty string. 
   - Go to jwt.io, apply your new header and payload, and in the signature box, ensure the secret is completely empty.
   - Ensure the "secret base64 encoded" checkbox is off.
5. Submit: The server reads an empty string, compares it to your empty-string signature, and grants access.