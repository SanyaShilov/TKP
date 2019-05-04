# pylint: disable = invalid-name, global-statement

import asyncio
from motor import motor_asyncio
import json
import os
import pymongo


async def generate_id(name):
    inc = await increment.find_one_and_update(
        {
            'id': 1
        },
        {
            '$inc': {
                name: 1
            }
        },
        new=True,
        upsert=True
    )
    return inc[name]


old_insert_one = motor_asyncio.AsyncIOMotorCollection.insert_one
old_insert_many = motor_asyncio.AsyncIOMotorCollection.insert_many


async def insert_one(self, document, **kwargs):
    if 'id' not in document:
        document['id'] = await generate_id(self.name)
    result = await old_insert_one(self, document, **kwargs)
    return {**document, '_id': result.inserted_id}


async def insert_many(self, documents, **kwargs):
    for document in documents:
        if 'id' not in document:
            document['id'] = await generate_id(self.name)
    result = await old_insert_many(self, documents, **kwargs)
    return [{**document, '_id': inserted_id} for document, inserted_id in zip(documents, result.inserted_ids)]


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
increment = db.increment


collections_dict = {}
collection_names = []
collections = []


def get_collections():
    global collections, collection_names, collections_dict

    collections_dict = {
        k: v for k, v in globals().items()
        if isinstance(v, motor_asyncio.AsyncIOMotorCollection)
    }
    collection_names, collections = zip(*((k, v) for k, v in collections_dict.items()))


get_collections()


async def amain():
    await add_validators()
    await create_indices()


async def create_indices():
    await users.create_index(
        'login',
        unique=True
    )
    for collection in collections:
        await collection.create_index(
            'id',
            unique=True
        )


async def add_validator(name, dirname):
    with open(os.path.join(dirname, 'validators', '{}.json'.format(name))) as file:
        validator = json.load(file)
        await db.command(
            'collMod',
            name,
            validator={
                '$jsonSchema': validator
            },
        )


async def hack_validator(collection):
    await collection.find_one_and_update(
        {'some': 'data'},
        {'$set': {'some': 'data'}},
        upsert=True
    )
    await collection.delete_one(
        {'some': 'data'}
    )


async def add_validators():
    dirname = os.path.dirname(__file__)
    for name, collection in collections_dict.items():
        try:
            await add_validator(name, dirname)
        except FileNotFoundError:
            pass
        except pymongo.errors.OperationFailure:
            await hack_validator(collection)
            await add_validator(name, dirname)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())


if __name__ == '__main__':
    main()
