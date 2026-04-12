# Node 02: The Weak Link

**Writeup-DB Academy - Infiltration Protocol**

You've bypassed the perimeter, but Node 02 enforces strict signature validation. The cryptography here is mathematically sound, but human error is always the weakest link in any system.

## Objective
Forge a valid admin token by discovering the system's symmetric signing key. Submit your forged token to the `/admin` endpoint to capture the flag.

## Vulnerability Profile
* **Category:** Cryptographic Weakness
* **Vector:** Offline Brute-Forcing (Weak Secret)

## Intel
The system administrators were lazy. They used a symmetric key (`HS256`) but chose a secret that is highly susceptible to dictionary attacks. 

**Tools required:**
* JWT cracking utility (Hashcat, John the Ripper, or a custom Python script)
* A standard wordlist (e.g., `rockyou.txt`)