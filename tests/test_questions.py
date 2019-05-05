import pytest


async def test_all_questions(fake_client):
    response = await fake_client.get(
        '/api/questions'
    )
    assert await response.json() == [
        {
            'id': 1,
            'content': 'question'
        }
    ]


@pytest.mark.parametrize(
    ['question_id', 'expected_response'],
    [
        [
            1,
            {
                'id': 1,
                'content': 'question'
            }
        ],
        [
            2,
            None
        ]
    ]
)
async def test_question_by_id(fake_client, question_id, expected_response):
    response = await fake_client.get(
        '/api/questions/byID',
        params={
            'id': question_id
        }
    )
    assert await response.json() == expected_response


async def test_insert_questions(fake_client):
    response = await fake_client.post(
        '/api/questions/insert',
        json={
            'content': 'some content'
        }
    )
    assert await response.json() == {
        'id': 2,
        'content': 'some content'
    }


async def test_delete_question(fake_client, db):
    response = await fake_client.post(
        '/api/questions/delete',
        params={
            'id': 1
        }
    )
    assert await response.json() == {}
    assert await db.questions.count_documents({}) == 0
