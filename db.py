# pylint: disable = invalid-name

import asyncio
from motor import motor_asyncio


client = motor_asyncio.AsyncIOMotorClient()
db = client.db

users = db.users


async def amain():
    await users.drop()
    await users.create_index(
        'login',
        unique=True
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())


if __name__ == '__main__':
    pass
