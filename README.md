# JWT-101-Lab: Token Heist by @touhidshaikh22

Welcome to Project Jwt 101. This vulnerable environment is designed to provide hands-on experience with the attack vectors associated with JSON Web Tokens (JWT, JWS, and JWE).

Jack into the system, intercept the tokens, and manipulate the cryptography to escalate your privileges across six distinct, isolated nodes.
<img width="1638" height="928" alt="image" src="https://github.com/user-attachments/assets/16db5c76-634e-4793-b9d7-46c7ab0ab21b" />


## System Architecture
This lab is built on a microservices architecture to mimic production environments. An Nginx API Gateway acts as the central dispatcher, routing traffic to six independent, vulnerable Python (Flask) containers.
- Gateway: Nginx Reverse Proxy (Port 80)
- Compute: 6x Python 3.10-slim containers running Gunicorn WSGI.
- Orchestration: Docker Compose

## Prerequisites
To deploy and interact with this environment, you will need the following tools:
- Docker and Docker Compose
- An interception proxy (e.g., Burp Suite Community/Professional)
- A local scripting environment (Python 3 recommended for cryptographic payload generation)
- Offline cracking tools (Hashcat or John the Ripper)

## Deployment Instructions
Clone this repository to your local machine and use Docker Compose to spin up the neural net.
```bash
git clone https://github.com/Writeup-DB/JWT-101-Lab.git
cd JWT-101-Lab
docker-compose up --build -d
docker-compose ps # Verify all 7 containers (1 Proxy + 6 Challenges) are running
```
The lab is now accessible at `http://localhost`. All traffic must be routed through this entry point.

## The Challenges
The gateway routes to different challenges based on the URL path. Your objective in each node is to escalate from a guest role to an admin role and retrieve the environment flag.

- **Challenges 1:** The Null Cipher (/chal1/) - The backend fails to enforce strict cryptographic standards. Intercept the standard token, manipulate the header to use the none algorithm, and forge an admin payload.

- **Challenges 2:** The Weak Link (/chal2/) - The signature is cryptographically sound, but the human element failed. Capture the token and utilize offline dictionary attacks to uncover the weak symmetric key.

- **Challenges 3:** The Ghost in the Path (/chal3/) - The application dynamically loads verification keys based on user input. Exploit a Path Traversal vulnerability via the kid header to force the server to verify against an empty file.

- **Challenges 4:** The Hydra (/chal4/) - This node utilizes JWS JSON Serialization for complex workflows. Exploit a logical flaw in the multi-signature validation loop to inject a rogue signature and bypass access controls.

- **Challenges 5:** The Doppelgänger (/chal5/) - The server expects asymmetric RS256 signatures. Force an Algorithm Confusion attack by switching the header to HS256 and signing your payload with the server's own public key.

- **Challenges 6:** The Remote Hijack (/chal6/) - The backend dynamically fetches public keys based on the jku header. Host a malicious JSON Web Key Set (JWKS) and redirect the server to trust your rogue cryptographic material.

## Teardown
To stop the containers and remove the isolated network, run the following command in the root directory:
```bash
docker-compose down
```

## Private and Public Key Gen
1. Generate the Private Key: `openssl genrsa -out private.pem 2048`
2. Extract the Public Key: `openssl rsa -in private.pem -pubout -out public.pem`

## Disclaimer
This project is created strictly for educational purposes and authorized security research. The vulnerabilities demonstrated here are intentionally implemented. Do not deploy this application in a production environment or expose it to the public internet without strict access controls. Always obtain explicit permission before testing external systems.
