from aiohttp import web
import json


def create_error_middleware(overrides):
    @web.middleware
    async def error_middleware(request, handler):

        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override:
                return await override(request, response.message)

            return response

        except json.decoder.JSONDecodeError as ex:
            return await overrides.get(400)(request, ex.msg)

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request, ex.reason)
            raise

    return error_middleware


async def handle_bad_request_error(request, details):
    return web.json_response({
        'error': 'Bad request',
        'description': 'The server isn\'t able to parse the given input',
        'details': details,
    }, status=400)


async def handle_not_found_error(request, details):
    return web.json_response({
        'error': 'Resource not found',
        'details': details,
    }, status=404)


async def handle_unprocessable_entity_error(request, details):
    return web.json_response({
        'error': 'Unprocessable entity',
        'description': 'The server understands the structure of the given input, but its semantics is invalid',
        'details': details,
    }, status=422)


async def handle_server_error(request, details):
    return web.json_response({
        'error': 'Server error',
        'details': details,
    }, status=500)


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        400: handle_bad_request_error,
        404: handle_not_found_error,
        422: handle_unprocessable_entity_error,
        500: handle_server_error
    })
    app.middlewares.append(error_middleware)
