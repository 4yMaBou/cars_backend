from models.code import Code
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from enum import IntFlag, auto
from datetime import datetime

class CodeStatus(IntFlag):
    NONE = 0 
    
    VALID = auto()
    NOT_USED = auto()
    
    OK = VALID | NOT_USED

async def check_code(value: str, db: AsyncSession) -> bool:
    status = CodeStatus.NONE
    
    try:
        query = select(Code).filter(Code.uuid == value).order_by(Code.timestamp.desc()).limit(1)
    except ValueError:
        return False
    
    query = await db.execute(query)
    code = query.scalar_one_or_none()

    status |=  CodeStatus.VALID * (code is not None)
    status |=  CodeStatus.NOT_USED * (not code.is_used)
    #print(f"status: {status:08b}")
    if status == CodeStatus.OK:
        code.is_used = True
        await db.commit()
        return True

    return False
    
async def list_codes(db: AsyncSession) -> list[Code]:
    query = select(Code).order_by(Code.timestamp.desc())
    codes = await db.execute(query)
    return list(codes.scalars().all())

async def create_code(db: AsyncSession) -> Code:
    value = uuid.uuid4()
    code = Code(uuid=value, is_used=False, timestamp=datetime.now())
    db.add(code)
    await db.commit()
    return code

async def delete_codes(timestamp: datetime, db: AsyncSession) -> None:
    query = delete(Code).filter(Code.timestamp < timestamp)
    await db.execute(query)
    await db.commit()
    return None