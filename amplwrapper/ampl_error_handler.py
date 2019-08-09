from amplpy import ErrorHandler
import logging


class AMPLErrorHandler(ErrorHandler):
    def error(self, exception):
        logging.log(logging.DEBUG, 'AMPL Error:', exception.getMessage())

    def warning(self, exception):
        logging.log(logging.DEBUG, 'AMPL Warning:', exception.getMessage())
