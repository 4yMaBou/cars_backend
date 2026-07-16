from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
import asyncio

KEYS_DIR = Path("keys/")
PRIVATE_PATH = KEYS_DIR / "private"
PUBLIC_PATH = KEYS_DIR / "public.pub"

async def write_keys() -> None:
    print("Writing keys...")
    KEYS_DIR.mkdir(exist_ok=True)
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    PRIVATE_PATH.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    PRIVATE_PATH.chmod(0o600)

    PUBLIC_PATH.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
    )


def read_keys() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    private_key = Ed25519PrivateKey.from_private_bytes(PRIVATE_PATH.read_bytes())
    public_key = Ed25519PublicKey.from_public_bytes(PUBLIC_PATH.read_bytes())
    return private_key, public_key

