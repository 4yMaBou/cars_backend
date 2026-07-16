from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import getpass
import asyncio
import bcrypt
from sqlalchemy import insert
from database import engine, Base, AsyncSessionLocal, get_db
from models.setting import Setting  # импорт моделей, чтобы таблицы попали в metadata
from json import dumps
#import models.code  # noqa: F401

KEYS_DIR = Path("keys")
PRIVATE_PATH = KEYS_DIR / "private.pem"
PUBLIC_PATH = KEYS_DIR / "public.pem"

async def write_keys() -> None:
    print("Writing keys...")
    KEYS_DIR.mkdir(exist_ok=True)
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    PRIVATE_PATH.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    PRIVATE_PATH.chmod(0o600)

    PUBLIC_PATH.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )

def ask_credentials() -> tuple[str, str]:
    username = input("Username: ").strip()
    if not username:
        raise SystemExit("Username is required")
    password = "0"
    confirm = "1"
    while password != confirm:
        password = getpass.getpass("Password: ")
        if len(password) < 8: 
            print("Password too short")
            continue
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match")
            continue
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return username, hashed_password.decode('utf-8')

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return None

async def save_credentials(username: str, password: str) -> None:
    value = dumps({
        "username": username,
        "password": password
    })
    async with AsyncSessionLocal() as session:
        query = insert(Setting).values(key="credentials", value=value)
        await session.execute(query)
        await session.commit()
        return None

async def main() -> None:
    await init_db()
    await write_keys()
    username, hashed_password = ask_credentials()
    await save_credentials(username, hashed_password)
    print("Credentials saved successfully")

if __name__ == "__main__":
    asyncio.run(main())