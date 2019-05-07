from aiohttp import web

import db
import utils


async def all_answers(request: web.Request) -> web.Response:
    answers = await db.answers.find(
        {},
        {
            '_id': False,
            'keyword_string': False
        }
    ).sort([('id', 1)]).to_list(None)
    return web.json_response(answers)


async def answers_for_question(request: web.Request) -> web.Response:
    question_id = int(request.query['questionID'])
    communications = await db.communications.find(
        {
            'questionID': question_id
        },
        {
            'answerID': True,
            '_id': False
        }
    ).to_list(None)
    answer_ids = [communication['answerID'] for communication in communications]
    answers = await db.answers.find(
        {
            'id': {
                '$in': answer_ids
            }
        },
        {
            '_id': False,
            'keyword_string': False
        }
    ).to_list(None)
    return web.json_response(answers)


async def answer_by_id(request: web.Request) -> web.Response:
    answer_id = int(request.query['id'])
    answer = await db.answers.find_one(
        {
            'id': answer_id
        },
        {
            '_id': False,
            'keyword_string': False
        }
    )  # or {}
    return web.json_response(answer)


async def insert_answer(request: web.Request) -> web.Response:
    data = await request.json()
    content = data['content']
    answer = await db.answers.insert_one(
        {
            'content': content,
            'keyword_string': utils.keyword_string(content)
        }
    )
    del answer['_id']
    del answer['keyword_string']
    return web.json_response(answer)


async def delete_answer(request: web.Request) -> web.Response:
    answer_id = int(request.query['id'])
    await db.answers.delete_one(
        {
            'id': answer_id
        }
    )
    return web.json_response({})


async def delete_old_answers():
    communications = await db.communications.find(
        {},
        {
            'answerID': True,
            '_id': False
        }
    ).to_list(None)
    communication_keys = await db.communication_keys.find(
        {},
        {
            'answerID': True,
            '_id': False
        }
    ).to_list(None)
    answer_ids = [
        comm['answerID']
        for comm in communications + communication_keys
    ]
    await db.answers.delete_many(
        {
            'id': {
                '$nin': answer_ids
            }
        }
    )
