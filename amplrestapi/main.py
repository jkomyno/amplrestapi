import logging
from ampljit import model as jit_model
from aiohttp import web
from asyncio import iscoroutine

from amplrestapi.jit.route_handler import JITRouteHandler
from amplwrapper.ampl_wrapper import AMPLWrapper
from config.config import Config
from amplrestapi.routes import setup_routes
from amplrestapi.middlewares import setup_middlewares


def setup_cleanup_hooks(tasks):
    async def cleanup():
        for func in tasks:
            result = func()
            if iscoroutine(result):
                await result

    return cleanup


def init():
    app = web.Application()

    # Initializes the JIT problem solver route
    jit_solver = jit_model.solve
    jit_handler = JITRouteHandler(ampl=AMPLWrapper(), solver=jit_solver)

    # Sets up the server routes
    setup_routes(app, jit_handler=jit_handler)

    # Sets up the server middleware methods
    setup_middlewares(app)

    # Declares the methods to call on server shutdown
    app.on_cleanup.append(setup_cleanup_hooks([
        jit_handler.on_exit,
    ]))

    # Reads the host and the port of the server from the config package
    host, port = Config.host(), Config.port()
    return app, host, port


def main():
    logging.basicConfig(level=logging.DEBUG)

    app, host, port = init()
    logging.log(logging.DEBUG, f'Running app on {host}:{str(port)}...')
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
