from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.setting import Setting

async def query_locale(db: AsyncSession):
    query = select(Setting).where(Setting.key == "locale")
    query = await db.execute(query)
    locale = query.scalar_one_or_none()
    if locale is None:
        raise ValueError
    return locale