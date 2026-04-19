import jwt
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

public_pem = b"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCF/K9NeE8Buf049NJpyTsN1uec
rMK6UuMyLP6Yw6DoOQRukEwRfJq1zPJ5/cbgcR4TTf7dRqhNgvrA4idEsETLc5UH
3FIWFb6kho+LmOyCpE+FJ0VqUTPWkdS3LU4zX9xpfdRFM2o1+LErCJNmVLuCOxYF
qAz4PHL9SyfzWRryZwIDAQAB
-----END PUBLIC KEY-----"""

# Load the public key
public_key = serialization.load_pem_public_key(public_pem, backend=default_backend())

# Convert to JWK format
jwk = jwt.algorithms.RSAAlgorithm.to_jwk(public_key)

# Wrap it in a Key Set (JWKS)
jwks = {
    "keys": [
        {
            **json.loads(jwk),
            "kid": "rogue-key-01",
            "use": "sig"
        }
    ]
}

print(json.dumps(jwks, indent=2))