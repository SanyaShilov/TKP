# pylint: disable = invalid-name, global-statement

import asyncio
from motor import motor_asyncio
import bson
import json
import os


def generate_id():
    return int(str(bson.ObjectId())[-7:], base=16)


old_insert_one = motor_asyncio.AsyncIOMotorCollection.insert_one
old_insert_many = motor_asyncio.AsyncIOMotorCollection.insert_many


async def insert_one(self, document, **kwargs):
    document.setdefault('id', generate_id())
    return await old_insert_one(self, document, **kwargs)


async def insert_many(self, documents, **kwargs):
    for document in documents:
        document.setdefault('id', generate_id())
    return await old_insert_many(self, documents, **kwargs)


motor_asyncio.AsyncIOMotorCollection.insert_many = insert_many
motor_asyncio.AsyncIOMotorCollection.insert_one = insert_one


client = motor_asyncio.AsyncIOMotorClient()
db = client.db

users = db.users
questions = db.questions
answers = db.answers
keywords = db.keywords
communications = db.communications
communication_keys = db.communication_keys
commands = db.commands


collections_dict = {}
collection_names = []
collections = []


def get_collections():
    global collections, collection_names, collections_dict

    collections_dict = {
        k: v for k, v in globals().items()
        if isinstance(v, motor_asyncio.AsyncIOMotorCollection)
    }
    collection_names, collections = zip(*(((k, v) for k, v in collections_dict.items())))


get_collections()


async def amain():
    await add_validators()
    await create_indices()


async def create_indices():
    await users.create_index(
        'login',
        unique=True
    )


async def add_validators():
    dirname = os.path.dirname(__file__)
    for name in collection_names:
        try:
            with open(os.path.join(dirname, 'validators', '{}.json'.format(name))) as file:
                validator = json.load(file)
                await db.command(
                    'collMod',
                    name,
                    validator={
                        '$jsonSchema': validator
                    },
                )
        except FileNotFoundError:
            pass


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())


if __name__ == '__main__':
    main()
