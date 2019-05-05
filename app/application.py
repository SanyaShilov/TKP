from aiohttp import web

from app import answers
from app import other
from app import questions


class Application(web.Application):
    def __init__(self):
        super().__init__()

        # answers
        self.router.add_get(
            '/api/answers',
            answers.all_answers
        )
        self.router.add_get(
            '/api/answers/answersForQuestion',
            answers.answers_for_question
        )
        self.router.add_get(
            '/api/answers/byID',
            answers.answer_by_id
        )
        self.router.add_post(
            '/api/answers/insert',
            answers.insert_answer
        )
        self.router.add_post(
            '/api/answers/delete',
            answers.delete_answer
        )

        # other
        self.router.add_post(
            '/api/register',
            other.register
        )
        self.router.add_post(
            '/api/login',
            other.login
        )
        self.router.add_post(
            '/api/request',
            other.api_request
        )
        self.router.add_post(
            '/api/evaluation',
            other.evaluation
        )
        self.router.add_static(
            '/docs/',
            '/data/static/',
            show_index=True
        )

        # questions
        self.router.add_get(
            '/api/questions',
            questions.all_questions
        )
        self.router.add_get(
            '/api/questions/byID',
            questions.question_by_id
        )
        self.router.add_post(
            '/api/questions/insert',
            questions.insert_question
        )
        self.router.add_post(
            '/api/questions/delete',
            questions.delete_question
        )
