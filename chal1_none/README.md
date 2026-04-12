# Node 01: The Null Cipher

**Welcome to the Writeup-DB Academy.**

Your first target is the perimeter gateway. It uses JSON Web Tokens for access control, but the implementation relies on outdated and flawed validation logic.

## Objective
Escalate your privileges from `guest` to `admin` and retrieve the flag from the `/admin` endpoint.

## Vulnerability Profile
* **Category:** Signature Bypass
* **Vector:** The `none` Algorithm

## Intel
The system's JWT library attempts to be overly accommodating. If a client explicitly tells the server not to verify the signature, the server might just listen. 

**Tools required:** * A proxy (Burp Suite / ZAP) or `cURL`
* Base64 encoder/decoder (or jwt.io)

*Good luck, Initiate.*