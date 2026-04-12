# Node 03: The Ghost in the Path

**Writeup-DB Academy - Lateral Movement**

This node utilizes a multi-key environment. The JWT header explicitly tells the backend which key file to use from the system's databanks to verify the token. 

## Objective
Exploit the key retrieval mechanism to bypass signature verification, gain `admin` access, and extract the flag.

## Vulnerability Profile
* **Category:** Header Parameter Injection
* **Vector:** `kid` (Key ID) Path Traversal

## Intel
The `kid` header is processed before the signature is verified—a classic chicken-and-egg problem. If the server dynamically fetches the secret key from the local filesystem based on your input, what happens if you point it somewhere unexpected? Perhaps a file that is completely empty?

**Tools required:**
* Burp Suite / ZAP
* A custom script to generate the malicious token and sign it with an empty string.