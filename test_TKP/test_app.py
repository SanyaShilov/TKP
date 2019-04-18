import pytest


@pytest.mark.parametrize(
    ['data', 'expected_response', 'count'],
    [
        [
            {
                'login': 'login',
                'pass': 'pass'
            },
            {
                'error': 1,
                'msg': 'Логин login уже занят',
                'data': None
            },
            1
        ],
        [
            {
                'login': 'another_login',
                'pass': 'pass'
            },
            {
                'error': 0,
                'msg': '',
                'data': None
            },
            2
        ]
    ]
)
async def test_register(fake_client, db, data, expected_response, count):
    response = await fake_client.post(
        '/api/register',
        json=data
    )
    assert await response.json() == expected_response
    assert await db.users.count_documents({}) == count


@pytest.mark.parametrize(
    ['data', 'expected_response'],
    [
        [
            {
                'login': 'login',
                'pass': 'pass'
            },
            {
                'error': 0,
                'msg': '',
                'data': {
                    'id': 12345,
                    'login': 'login',
                    'pass': 'pass',
                    'some': 'data',
                },
            },
        ],
        [
            {
                'login': 'another_login',
                'pass': 'pass'
            },
            {
                'error': 1,
                'msg': 'Пользователь с логином another_login не найден',
                'data': None
            },
        ],
        [
            {
                'login': 'login',
                'pass': 'another_pass'
            },
            {
                'error': 2,
                'msg': 'Неверный пароль',
                'data': None
            },
        ]
    ]
)
async def test_login(fake_client, data, expected_response):
    response = await fake_client.post(
        '/api/login',
        json=data
    )
    assert await response.json() == expected_response


async def test_answer(fake_client):
    response = await fake_client.post(
        '/api/request',
        json={}
    )
    assert await response.json() == {
        'error': 0,
        'msg': '',
        'data': {
            'answer': 'answer',
            'communication': 1,
            'communication_key': 1,
        }
    }


async def test_evaluate(fake_client):
    response = await fake_client.post(
        '/api/evaluation',
        json={}
    )
    assert await response.json() == {
        'error': 0,
        'msg': '',
        'data': None
    }
