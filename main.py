import base64
from nacl.public import PrivateKey

def generate_wireguard_keys():
    private_key = PrivateKey.generate()
    public_key = private_key.public_key

    private_b64 = base64.b64encode(private_key.encode()).decode()
    public_b64  = base64.b64encode(public_key.encode()).decode()

    return private_b64, public_b64

priv, pub = generate_wireguard_keys()
print("Private:", priv)
print("Public :", pub)
