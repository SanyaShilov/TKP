from aiohttp import web

from app import answers
from app import other


class Application(web.Application):
    def __init__(self):
        super().__init__()

        self.router.add_get('/api/answers', answers.all_answers)
        self.router.add_get('/api/answers/answersForQuestion', answers.answers_for_question)
        self.router.add_get('/api/answers/byID', answers.answer_by_id)
        self.router.add_post('/api/answers/insert', answers.insert_answer)

        self.router.add_post('/api/register', other.register)
        self.router.add_post('/api/login', other.login)
        self.router.add_post('/api/request', other.request)
        self.router.add_post('/api/evaluation', other.evaluation)
        self.router.add_static('/docs/', '/data/static/', show_index=True)
