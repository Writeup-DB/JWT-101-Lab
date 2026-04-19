## Node 01: The Null Cipher (none Algorithm)
The backend fails to enforce signatures if the client explicitly requests the none algorithm.

1. Obtain the Token: Click "Initialize Connection" to get your standard guest token.
2. Decode the Token: Copy the token and paste it into a tool like jwt.io or decode it manually using base64.
3. Manipulate the Header: Change the algorithm from `HS256` to `none`.
```json
{
  "alg": "none",
  "typ": "JWT"
}
```
4. Manipulate the Payload: Elevate your privileges by changing `"role": "guest"` to `"role": "admin"`.
5. Re-encode and Strip: Base64URL encode your new header and payload. Concatenate them with a period `(.)`. Do not add a signature, but keep the trailing period.
   - **Format**: `ewogICJhbGciOiAibm9uZSIsCiAgInR5cCI6ICJKV1QiCn0.ewogICJ1c2VyIjogImd1ZXN0IiwKICAicm9sZSI6ICJhZG1pbiIKfQ.`
6. Submit: Paste this modified string into the Exploit console and submit.