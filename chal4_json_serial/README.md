# Node 04: The Hydra

**Writeup-DB Academy - Advanced Parsing**

Welcome to the deep web. Node 04 doesn't use the standard compact JWT string format (Header.Payload.Signature). It uses JWS JSON Serialization to handle complex, multi-signature workflows. 

## Objective
Manipulate the JSON structure to trick the validation loop into granting you `admin` access.

## Vulnerability Profile
* **Category:** Parsing Discrepancy / Logic Flaw
* **Vector:** Multi-Signature Bypass

## Intel
The payload claims you are a student. The server expects an admin signature. However, the system is designed to loop through an *array* of signatures. If it finds *any* mathematically valid signature for the given payload, it might stop checking the rest. Can you introduce a valid signature that the system trusts, even if it's not the admin's?

**Tools required:**
* Burp Suite Repeater
* Python (for generating valid HMAC signatures)