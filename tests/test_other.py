import pytest


@pytest.mark.parametrize(
    ['data', 'expected_response', 'ids'],
    [
        [
            {
                'realName': 'name',
                'login': 'login',
                'pass': 'pass',
                'age': 42,
                'city': 'city',
                'email': 'email',
                'lastEntry': 'today',
            },
            {
                'error': 1,
                'msg': 'Логин login уже занят',
                'data': None
            },
            [1]
        ],
        [
            {
                'realName': 'name',
                'login': 'another_login',
                'pass': 'pass',
                'age': 42,
                'city': 'city',
                'email': 'email',
                'lastEntry': 'today',
            },
            {
                'error': 0,
                'msg': '',
                'data': None
            },
            [1, 2]
        ]
    ]
)
async def test_register(fake_client, db, data, expected_response, ids):
    response = await fake_client.post(
        '/api/register',
        json=data
    )
    assert await response.json() == expected_response
    assert [user['id'] for user in await db.users.find().to_list(None)] == ids


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
                    'id': 1,
                    'realName': 'name',
                    'login': 'login',
                    'pass': 'pass',
                    'age': 42,
                    'city': 'city',
                    'email': 'email',
                    'lastEntry': 'today',
                    'admin': 1
                }
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


async def test_request(fake_client):
    response = await fake_client.post(
        '/api/request',
        json={
            'request': 'Где находится Эйфелева башня?'
        }
    )
    assert await response.json() == {
        'error': 0,
        'msg': '',
        'data': {
            'answer': 'Эйфелева башня находится в Париже',
            'question_id': 2
        }
    }


async def test_evaluation(fake_client):
    response = await fake_client.post(
        '/api/evaluation',
        json={
            'question_id': 1,
            'eval': 1
        }
    )
    assert await response.json() == {
        'error': 0,
        'msg': '',
        'data': None
    }


async def test_training(fake_client):
    response = await fake_client.post(
        '/api/request',
        json={
            'request': 'Где находится Эйфелева башня? ответ'
        }
    )
    body = await response.json()
    assert body['data']['answer'] == 'Эйфелева башня находится в Париже'
    await fake_client.post(
        '/api/evaluation',
        json={
            'question_id': body['data']['question_id'],
            'eval': -1
        }
    )
    response = await fake_client.post(
        '/api/request',
        json={
            'request': 'Где находится Эйфелева башня? ответ'
        }
    )
    body = await response.json()
    assert body['data']['answer'] == 'ответ'
    await fake_client.post(
        '/api/evaluation',
        json={
            'question_id': body['data']['question_id'],
            'eval': -1
        }
    )
    response = await fake_client.post(
        '/api/request',
        json={
            'request': 'Где находится Эйфелева башня? ответ'
        }
    )
    body = await response.json()
    assert body['data']['answer'] == 'Эйфелева башня находится в Париже'
