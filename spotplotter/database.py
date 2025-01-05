import asyncpg
from spotplotter.core.config import settings


class AsyncDatabase:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            settings.database_url, min_size=1, max_size=20
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def fetch_one(self, query, *args):
        if not self.pool:
            await self.connect()

        async with self.pool.acquire() as conn:  # type: ignore
            return await conn.fetchrow(query, *args)

    async def fetch_all(self, query, *args):
        if not self.pool:
            await self.connect()

        async with self.pool.acquire() as conn:  # type: ignore
            return await conn.fetch(query, *args)

    async def execute(self, query, *args):
        if not self.pool:
            await self.connect()

        async with self.pool.acquire() as conn:  # type: ignore
            return await conn.execute(query, *args)


# Create a global database instance
async_db = AsyncDatabase()
