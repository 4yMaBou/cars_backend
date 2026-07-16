import getpass
import asyncio
import bcrypt
from sqlalchemy import insert, delete
from database import engine, Base, AsyncSessionLocal
from models.setting import Setting  # импорт моделей, чтобы таблицы попали в metadata
from auth.keys import write_keys

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
    value = {
        "username": username,
        "password": password
    }
    async with AsyncSessionLocal() as session:
        query = delete(Setting).where(Setting.key == "credentials")
        await session.execute(query)
        await session.commit()
        
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