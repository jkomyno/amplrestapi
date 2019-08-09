from amplpy import AMPL

from amplwrapper.ampl_error_handler import AMPLErrorHandler
from amplwrapper.ampl_output_handler import AMPLOutputHandler


class AMPLWrapper:
    """
    References:
    - https://ampl.com/BOOK/CHAPTERS/17-solvers.pdf
    """

    def __init__(self):
        self._ampl = AMPL()

        """
        Use the CPLEX solver driver for linear programming problems.
        """
        self._ampl.setOption('solver', 'cplex')

        """
         Prevent using the current values as well as the statuses of the variables in
         constructing the starting point at the next solve.
        """
        self._ampl.setOption('reset_initial_guesses', True)

        """
        The major use of solver status values from an optimal basic solution is to provide a
        good starting point for the next optimization run. The option send_statuses, when set to True,
        instructs AMPL to include statuses with the information about variables sent to the solver at each solve.
        """
        self._ampl.setOption('send_statuses', True)

        self._n_iterations: int = 0

        """
        Add class that handles AMPL outputs
        """
        self._ampl.setOutputHandler(AMPLOutputHandler(self.set_n_iterations))

        """
        Add class that handles errors and warnings that may occur during the AMPL execution.
        """
        self._ampl.setErrorHandler(AMPLErrorHandler())

    def set_n_iterations(self, iterations):
        self._n_iterations = iterations

    @property
    def n_iterations(self):
        return self._n_iterations

    @property
    def ampl(self):
        return self._ampl

    def reset(self):
        self.ampl.reset()

    def eval(self, statements: str):
        self.ampl.eval(statements)

    def solve(self) -> float:
        from time import time
        # Wait for the solution to complete
        start = time()
        self.ampl.solve()
        computation_duration = time() - start
        return computation_duration

    def get_parameter(self, parameter):
        return self.ampl.getParameter(parameter)

    def get_variable_value(self, variable):
        return self.ampl.getVariable(variable).value()

    def get_variable_values(self, variable):
        return self.ampl.getVariable(variable).getValues()

    def get_value(self, scalar_expression):
        """
        Get a scalar value from the underlying AMPL interpreter, as a double or
        a string.

        Args:
            scalar_expression: An AMPL expression which evaluates to a scalar
            value.

        Returns:
            The value of the expression.
        """
        return self.ampl.getValue(scalar_expression)

    def set_data(self, data, set_name=None):
        """
        Assign the data in the dataframe to the AMPL entities with the names
        corresponding to the column names.

        Args:
            data: The dataframe containing the data to be assigned.

            set_name: The name of the set to which the indices values of the
            DataFrame are to be assigned.

        Raises:
            AMPLException: if the data assignment procedure was not successful.
        """
        self.ampl.setData(data, set_name)

    def close(self):
        """
        Deletes the Ampl object.
        From the Amplpy docs:
        "The [AMPL] object is quite resource-heavy, therefore it should be explicitly closed as soon
        as it is not needed anymore"
        """
        self.ampl.close()
