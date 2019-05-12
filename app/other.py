from aiohttp import web
import operator

import pymongo

import db
import utils


async def register(request: web.Request) -> web.Response:
    data = await request.json()
    data.setdefault('admin', 0)
    error = 0
    msg = ''
    try:
        await db.users.insert_one(data)
    except pymongo.errors.DuplicateKeyError:
        error = 1
        msg = 'Логин {} уже занят'.format(data['login'])
    return web.json_response(
        {
            'error': error,
            'msg': msg,
            'data': None
        }
    )


async def login(request: web.Request) -> web.Response:
    data = await request.json()
    error = 0
    msg = ''
    return_data = None
    user = await db.users.find_one(
        {
            'login': data['login']
        },
        {
            '_id': False
        }
    )
    if not user:
        error = 1
        msg = 'Пользователь с логином {} не найден'.format(data['login'])
    elif user['pass'] != data['pass']:
        error = 2
        msg = 'Неверный пароль'
    else:
        return_data = user
    return web.json_response(
        {
            'error': error,
            'msg': msg,
            'data': return_data
        }
    )


async def api_request(request: web.Request) -> web.Response:
    data = await request.json()
    question_content = data['content']
    keyword_string = utils.keyword_string(question_content)
    answers = await db.answers.find(
        {
            '$text': {
                '$search': keyword_string
            }
        },
        {
            'score': {
                '$meta': 'textScore'
            }
        }
    ).sort([('id', 1)]).to_list(None)
    if not answers:
        answer = 'Не знаю'
        inserted_question_id = 0
    else:
        answer_ids = [answer['id'] for answer in answers]
        questions = await db.questions.find(
            {
                'answer_id': {
                    '$in': answer_ids
                },
                'eval': {
                    '$exists': True
                },
                '$text': {
                    '$search': keyword_string
                }
            },
            {
                'score': {
                    '$meta': 'textScore'
                }
            }
        ).sort([('answer_id', 1)]).to_list(None)
        index = 0
        for question in questions:
            answer_id = question['answer_id']
            while answers[index]['id'] != answer_id:
                index += 1
            answers[index]['score'] += question['score'] * question['eval']
        answers.sort(key=operator.itemgetter('score'), reverse=True)
        answer = answers[0]['content']
        inserted_question = await db.questions.insert_one(
            {
                'content': question_content,
                'keyword_string': keyword_string,
                'answer_id': answers[0]['id']
            }
        )
        inserted_question_id = inserted_question['id']
    response = {
        'error': 0,
        'msg': '',
        'data': {
            'answer': answer,
        }
    }
    if inserted_question_id:
        response['data']['question_id'] = inserted_question_id
    return web.json_response(response)


async def evaluation(request: web.Request) -> web.Response:
    data = await request.json()
    await db.questions.find_one_and_update(
        {
            'id': data['question_id']
        },
        {
            '$set': {
                'eval': data['eval']
            }
        }
    )
    return web.json_response(
        {
            'error': 0,
            'msg': '',
            'data': None
        }
    )
