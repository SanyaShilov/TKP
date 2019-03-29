import asyncio
from motor import motor_asyncio


_client = motor_asyncio.AsyncIOMotorClient()
_db = _client.db

users = _db.users


async def main():
    await users.drop()
    await users.create_index(
        'login',
        unique=True
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
