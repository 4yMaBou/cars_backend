from models.code import Code
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from enum import IntFlag, auto

class CodeStatus(IntFlag):
    NONE = 0 
    
    VALID = auto()
    NOT_USED = auto()
    
    OK = VALID | NOT_USED

async def check_code(value: str, db: AsyncSession) -> bool:
    status = CodeStatus.NONE
    
    try:
        query = select(Code).filter(Code.uuid == uuid.UUID(value)).order_by(Code.datetime.desc()).limit(1)
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
    
