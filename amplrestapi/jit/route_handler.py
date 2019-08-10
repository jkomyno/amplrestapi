from os import path
from aiohttp import web, web_request
from asyncio import Lock
import json

from ampljit import model as jit_model
from amplrestapi.abstract_ampl_routes_handler import AbstractAMPLRoutesHandler
from amplrestapi.http_validation_error import HTTPValidationError
from amplrestapi.jit.validate import validate
from amplwrapper.ampl_wrapper import AMPLWrapper

json_schema: dict
with open(path.join(path.dirname(__file__), 'route_schema.json'), 'r') as json_schema_file:
    json_schema = json.load(json_schema_file)


class JITRouteHandler(AbstractAMPLRoutesHandler):
    """
    JITRoutesHandler exposes a REST interface for the dynamic Just-in-time computational problem.
    """

    def __init__(self, ampl: AMPLWrapper, solver: jit_model.solve):
        """
        :param ampl: AMPLWrapper instance
        :param solver: Function that solves the JIT problem using AMPL
        """
        super().__init__(ampl)
        self._solver = solver
        self._lock = Lock()

    async def run(self, request: web_request.Request):
        # read the input data from the POST body and check if it's written in a parseable format
        input_data = await request.json()

        # verify that the given data is semantically valid
        is_valid, err_message = validate(json=input_data, schema=json_schema)
        if not is_valid:
            raise HTTPValidationError(err_message)

        # extract variables from the input data
        n_batches: int = input_data['n_batches']
        wrong_time_fee: int = input_data['wrong_time_fee']
        duration_lst: list = input_data['duration']
        expected_finish_lst: list = input_data['expected_finish']

        # solve the problem in a critical section.
        # self.ampl is a shared resource whose access is regulated by an asyncio.Lock.
        async with self._lock:
            json_response = self._solver(ampl=self.ampl, n_batches=n_batches, wrong_time_fee=wrong_time_fee,
                                         duration_lst=duration_lst,
                                         expected_finish_datetime_str_lst=expected_finish_lst)

        # This block is outside of the previous critical section.
        # The computation results has been gathered and can be returned to the user.
        return web.json_response(json_response)

    def on_exit(self):
        self.ampl.close()
