from aiohttp.web_exceptions import HTTPClientError


class HTTPValidationError(HTTPClientError):
    status_code = 422

    def __init__(self, reason: str):
        super().__init__(reason=reason)
