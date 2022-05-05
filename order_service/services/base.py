from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save_transaction(self):
        try:
            await self.db_session.commit()
        except Exception:
            await self.db_session.rollback()
            raise
