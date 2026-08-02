# مزود الجلسات لقاعدة البيانات (AsyncSession Generator)
from typing import AsyncGenerator
from app.core.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator:
    """Dependency لتمرير جلسة قاعدة البيانات للـ Endpoints"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()