from aiohttp import web

import db


async def all_questions(request: web.Request) -> web.Response:
    questions = await db.questions.find(
        {},
        {
            '_id': False
        }
    ).to_list(None)
    return web.json_response(questions)


async def question_by_id(request: web.Request) -> web.Response:
    question_id = int(request.query['id'])
    question = await db.questions.find_one(
        {
            'id': question_id
        },
        {
            '_id': False
        }
    )  # or {}
    return web.json_response(question)


async def insert_question(request: web.Request) -> web.Response:
    data = await request.json()
    question = await db.questions.insert_one(
        {
            'content': data['content']
        }
    )
    del question['_id']
    return web.json_response(question)


async def delete_question(request: web.Request) -> web.Response:
    question_id = int(request.query['id'])
    await db.questions.delete_one(
        {
            'id': question_id
        }
    )
    # await communications.delete_communications_for_question(question_id)
    return web.json_response({})
