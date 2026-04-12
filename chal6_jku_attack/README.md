# Node 06: The Remote Hijack

**Writeup-DB Academy - The Core**

You have reached the final challenge. This system uses decentralized authentication. It relies on the `jku` (JSON Web Key Set URL) header to fetch the public keys required for token verification from an internal telemetry server.

## Objective
Force the server to authenticate your forged `admin` token by hijacking the key retrieval process. 

## Vulnerability Profile
* **Category:** Key Management Flaw
* **Vector:** `jku` Header Injection (Remote Key Hijacking)

## Intel
The system reads the `jku` header and makes an outbound HTTP request to fetch the keys. There is no whitelist. You must generate your own RSA keypair, host the public key in JWKS format on a server you control, and point the `jku` header to your rogue infrastructure.

**Tools required:**
* Publicly accessible web server (e.g., ngrok, Webhook.site, or a VPS)
* Scripting knowledge to generate an RSA keypair and format it as a JWK.