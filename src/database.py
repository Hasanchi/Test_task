from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DB_URL = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres'

async_engine = create_async_engine(DB_URL, echo=True)

async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
