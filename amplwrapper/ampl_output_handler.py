from amplpy import OutputHandler, Kind
from typing import Callable
import re
import logging


class AMPLOutputHandler(OutputHandler):
    """
    Object used as an output handler for AMPL. It only prints the solver output.
    It also parses the solver output message to capture the number of dual simplex
    iterations performed by the CPLEX solver. That number is dispatched to the
    object that instantiated this object via the `n_iterations_consumer` consumer function.
    """

    def __init__(self, n_iterations_consumer: Callable[[int], None]):
        self.n_iterations_consumer = n_iterations_consumer

    def output(self, kind, msg):
        if kind == Kind.SOLVE:
            regex = re.compile(r'([0-9]+) dual simplex iterations', re.MULTILINE)
            matches = re.findall(regex, msg)
            logging.log(logging.DEBUG, msg)

            if len(matches) > 0:
                n_iterations = int(matches[0])
                self.n_iterations_consumer(n_iterations)
