# Node 05: The Doppelgänger

**Writeup-DB Academy - Cryptographic Confusion**

This node is hardened. It uses asymmetric cryptography (`RS256`) for token signing. The private key is secured offline, but the public key is available for clients to verify tokens themselves.

## Objective
Exploit the algorithm validation logic to forge an `admin` token using only the publicly available information.

## Vulnerability Profile
* **Category:** Cryptographic Flaw
* **Vector:** Algorithm Confusion (`RS256` to `HS256`)

## Intel
The validation library blindly trusts the `alg` header provided by the user. If you switch the algorithm to `HS256` (symmetric), the backend will attempt to verify the HMAC signature. But what secret will it use? It will grab the only key it knows: the *Public Key* string. 

**Tools required:**
* Burp Suite
* A script to read the PEM file and use it as an HMAC symmetric secret.