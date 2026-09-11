import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker
from api.database import engine
from api.services.auth_service import get_password_hash, generate_api_key
from api.models.user import User

async def main():
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        # Check if exists
        from sqlalchemy import select
        result = await session.execute(select(User).filter(User.email == "admin@onionbyte.com"))
        if not result.scalars().first():
            user = User(
                email="admin@onionbyte.com",
                hashed_password=get_password_hash("admin1234"),
                company_name="Onion Byte Admin",
                plan="pro",
                api_key=generate_api_key()
            )
            session.add(user)
            await session.commit()
            print("Admin account created successfully!")
        else:
            print("Admin account already exists.")

if __name__ == "__main__":
    asyncio.run(main())
