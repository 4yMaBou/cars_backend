from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
     "sqlite+aiosqlite:///./cars.db",
     connect_args={"check_same_thread": False},
 )

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False   
)

class Base(DeclarativeBase):
     pass

async def get_db():
     db = AsyncSessionLocal()
     try:
         yield db
     finally:
         await db.close()