from aiohttp import web

from amplrestapi.abstract_ampl_routes_handler import AbstractAMPLRoutesHandler


def setup_routes(app: web.Application, jit_handler: AbstractAMPLRoutesHandler):
    router = app.router
    router.add_post('/problems/jit', jit_handler.run)
    # router.add_get('/problems/investments-plan', handler.investments_plan)
    # router.add_get('/problems/knapsack', handler.knapsack)
