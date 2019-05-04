import argparse

from aiohttp import web
import pymongo

import db


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


async def answer(request: web.Request) -> web.Response:
    return web.json_response(
        {
            'error': 0,
            'msg': '',
            'data': {
                'answer': 'answer',
                'communication': 1,
                'communication_key': 1,
            }
        }
    )


async def evaluate(request: web.Request) -> web.Response:
    return web.json_response(
        {
            'error': 0,
            'msg': '',
            'data': None
        }
    )


class Application(web.Application):
    def __init__(self):
        super().__init__()
        self.router.add_post('/api/register', register)
        self.router.add_post('/api/login', login)
        self.router.add_post('/api/request', answer)
        self.router.add_post('/api/evaluation', evaluate)
        self.router.add_static('/docs/', '/data/static/', show_index=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8001)
    return parser.parse_args()


def main():
    app = Application()
    args = parse_args()
    web.run_app(app, port=args.port)


if __name__ == '__main__':
    main()
