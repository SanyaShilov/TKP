# pylint: disable = redefined-outer-name

import asyncio
import json

import bson
import pytest
from motor import motor_asyncio

import app
import db as db_module
import utils


PORT = 12345


@pytest.fixture(scope='session')
def monkeypatch_session():
    from _pytest.monkeypatch import MonkeyPatch
    monkeypatch = MonkeyPatch()
    yield monkeypatch
    monkeypatch.undo()


@pytest.fixture(autouse=True, scope='session')
def loop():
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    yield event_loop
    event_loop.close()


def convert(obj):
    if isinstance(obj, dict):
        if '$oid' in obj:
            return bson.ObjectId(obj['$oid'])
        if '$date' in obj:
            return utils.parse_timestring(obj['$date'])
        return {
            key: convert(value) for key, value in obj.items()
        }
    if isinstance(obj, list):
        return [convert(item) for item in obj]
    return obj


async def fill_db(database, filename):
    file = open(filename)
    json_data = json.load(file)
    for key, value in json_data.items():
        await getattr(database, key).insert_many(convert(value))
    file.close()


@pytest.fixture(autouse=True, scope='session')
async def _patched_db(monkeypatch_session, loop):
    client = motor_asyncio.AsyncIOMotorClient(io_loop=loop)
    test_db = client.test_db

    monkeypatch_session.setattr(db_module, 'db', test_db)
    monkeypatch_session.setattr(db_module, 'users', test_db.users)

    await db_module.create_indices()

    return test_db


@pytest.fixture(autouse=True)
async def db(_patched_db, monkeypatch, loop):
    await _patched_db.users.delete_many({})

    await fill_db(_patched_db, './test_TKP/default_database.json')

    return _patched_db


@pytest.fixture(autouse=True)
def utcnow(monkeypatch):
    from freezegun import freeze_time

    freezer = freeze_time("2018-11-14 23:09:01")
    freezer.start()
    yield
    freezer.stop()


@pytest.fixture()
def oid(monkeypatch):
    const_object_id = bson.ObjectId('5be1e9ea4b3e4d0db08713b7')

    def get_oid():
        return const_object_id

    monkeypatch.setattr(bson, 'ObjectId', get_oid)
    return const_object_id


@pytest.fixture()
def fake_app():
    return app.Application()


@pytest.fixture()
async def fake_client(aiohttp_client, fake_app, monkeypatch):
    client = await aiohttp_client(
        fake_app, server_kwargs={'port': PORT}
    )
    return client
