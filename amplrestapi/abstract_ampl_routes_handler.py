from abc import ABC, abstractmethod
from aiohttp import web_request, web_response

from amplwrapper.ampl_wrapper import AMPLWrapper


class AbstractAMPLRoutesHandler(ABC):
    def __init__(self, ampl: AMPLWrapper):
        self._ampl: AMPLWrapper = ampl

    @property
    def ampl(self):
        return self._ampl

    @abstractmethod
    async def run(self, request: web_request.Request) -> web_response.Response:
        """
        This method should implement the logic of the REST request
        :param request: AIOHTTP object that represents a REST request
        :return: AIOHTTP response
        """
        pass

    @abstractmethod
    async def on_exit(self):
        """
        This hook method will be automatically called by AIOHTTP on server shutdown.
        It's en example of Dependency Inversion.
        """
        pass
