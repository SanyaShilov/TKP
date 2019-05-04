import pytest

from app import answers


async def test_all_answers(fake_client):
    response = await fake_client.get(
        '/api/answers'
    )
    assert await response.json() == [
        {
            'id': 1,
            'content': 'answer'
        }
    ]


@pytest.mark.parametrize(
    ['question_id', 'expected_response'],
    [
        [
            1,
            [
                {
                    'id': 1,
                    'content': 'answer'
                }
            ]
        ],
        [
            2,
            []
        ]
    ]
)
async def test_answers_for_question(fake_client, question_id, expected_response):
    response = await fake_client.get(
        '/api/answers/answersForQuestion',
        params={
            'questionID': question_id
        }
    )
    assert await response.json() == expected_response


@pytest.mark.parametrize(
    ['answer_id', 'expected_response'],
    [
        [
            1,
            {
                'id': 1,
                'content': 'answer'
            }
        ],
        [
            2,
            None
        ]
    ]
)
async def test_answer_by_id(fake_client, answer_id, expected_response):
    response = await fake_client.get(
        '/api/answers/byID',
        params={
            'id': answer_id
        }
    )
    assert await response.json() == expected_response


async def test_insert_answers(fake_client):
    response = await fake_client.post(
        '/api/answers/insert',
        json={
            'content': 'some content'
        }
    )
    assert await response.json() == {
        'id': 2,
        'content': 'some content'
    }


async def test_delete_old_answers(db):
    await db.answers.insert_one(
        {
            'content': 'answer 2'
        }
    )
    assert await db.answers.count_documents({}) == 2
    await answers.delete_old_answers()
    assert await db.answers.count_documents({}) == 1
