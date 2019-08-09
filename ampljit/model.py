from os import path
import logging
from amplpy import DataFrame

from ampljit import utils
from amplwrapper.ampl_wrapper import AMPLWrapper

models_directory = path.join(path.dirname(__file__), 'model')
model_filename = path.join(models_directory, 'jit.mod')

model_statements: str
with open(model_filename) as model_content:
    model_statements = model_content.read()


def solve(ampl: AMPLWrapper, n_batches: int, wrong_time_fee: int, duration_lst: list,
          expected_finish_datetime_str_lst: list, datetime_format: str = '%Y-%m-%d %H:%M'):
    # clear every data from the AMPL model
    ampl.reset()
    ampl.eval(model_statements)

    # read data from input
    ordering_st_constraints = utils.create_multiple_constraints(
        1,
        n_batches,
        create_constraints=utils.create_multiple_ordering_constraints
    )

    # converts strings in the ISO8601 format to datetime objects
    expected_finish_datetime_lst = utils.strings_to_datetimes(expected_finish_datetime_str_lst, datetime_format)

    # converts a list of datetime objects into a list of minute time deltas with respect to the first item
    expected_finish_lst = utils.minute_timedeltas_wrt_first(expected_finish_datetime_lst)

    logging.log(logging.DEBUG, f'Constraints: {ordering_st_constraints}')
    ampl.eval(ordering_st_constraints)

    batch_lst = utils.create_batch_list(n_batches)
    batch_dict = utils.create_batch_dictionary(
        batch_lst,
        duration_lst=duration_lst,
        expected_finish_lst=expected_finish_lst
    )
    batch_data = DataFrame.fromDict(batch_dict, index_names=['BATCH'], column_names=['duration', 'expected_finish'])

    logging.log(logging.DEBUG, 'Setting Batch values')
    logging.log(logging.DEBUG, f'batch_data: \n{batch_data}')

    # update the wrong_time_fee AMPL parameter
    wrong_time_fee_parameter = ampl.get_parameter('wrong_time_fee')
    wrong_time_fee_parameter.set(wrong_time_fee)

    # write the values of the BATCH set on AMPL
    ampl.set_data(batch_data, set_name='BATCH')

    # ask AMPL to solve the problem with the given data
    computation_duration = ampl.solve()

    # retrieve computed values and parameters from AMPL
    objective_value: int = ampl.get_value('total_fee')
    start_time: DataFrame = ampl.get_variable_values('start_time')
    delta_time: DataFrame = ampl.get_variable_values('delta_time')

    start_minutes = utils.dict_to_list(start_time.toDict())

    # convert start_minutes to a list of datetime objects
    start_datetime_lst = utils.set_minutes_to_datetimes(datetime_lst=expected_finish_datetime_lst,
                                                        minutes_lst=start_minutes)

    delta_time_lst = utils.dict_to_list(delta_time.toDict())

    result_batch_dict = utils.create_result_batch_dictionary(
        batch_lst,
        start_datetime_lst=start_minutes,
        delta_time_lst=delta_time_lst
    )
    result_batch_data = DataFrame.fromDict(result_batch_dict, index_names=['BATCH'],
                                           column_names=['start_datetime', 'delta_time'])
    logging.log(logging.DEBUG, f'result_batch_data: \n{result_batch_data}')

    return {
        'data': {
            'total_fee': objective_value,
            'start_datetime': utils.datetimes_to_strings(start_datetime_lst, datetime_format),
            'delta_time': delta_time_lst,
        },
        'meta': {
            'iterations': ampl.n_iterations,
            'computation_duration': computation_duration,
        },
    }
