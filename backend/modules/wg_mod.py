import os
import base64
from nacl.public import PrivateKey
from dotenv import load_dotenv

load_dotenv()

def keys_match(private_b64: str, public_b64: str) -> bool:
    private_bytes = base64.b64decode(private_b64)
    public_bytes = base64.b64decode(public_b64)

    private_key = PrivateKey(private_bytes)
    derived_public = private_key.public_key.encode()

    return derived_public == public_bytes

def generate_client_key() -> dict:
    private_key = PrivateKey.generate()
    public_key = private_key.public_key

    private_b64 = base64.b64encode(private_key.encode()).decode()
    public_b64  = base64.b64encode(public_key.encode()).decode()

    return private_b64, public_b64

def generate_client_psk() -> str:
    psk_bytes = os.urandom(32)
    psk_b64 = base64.b64encode(psk_bytes).decode()
    return psk_b64