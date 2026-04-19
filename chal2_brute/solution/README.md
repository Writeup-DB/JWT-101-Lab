## Node 02: The Weak Link (Brute-Forcing)
The token is cryptographically sound, but the human-chosen password is weak.

1. Obtain the Token: Get the initial guest token.
2. Save to File: Save the raw token string into a text file named hash.txt.
3. Crack the Secret: Use hashcat and a standard wordlist (like rockyou.txt) to crack the HMAC secret.
```bash
hashcat -a 0 -m 16500 hash.txt rockyou.txt
```
*Result: Hashcat will reveal the secret key is `shadow`.*

4. Forge the Token: Go to jwt.io. Paste your original token. Change the payload to "role": "admin". In the "Verify Signature" section at the bottom, enter the cracked secret: `shadow`.
5. Submit: Copy the newly generated, validly signed token and submit it.