from datetime import datetime, timedelta
from typing import Callable


def create_batch_list(n_batches: int) -> list:
    return list(map(lambda x: x, range(1, n_batches + 1)))


def create_batch_dictionary(batch_lst: list, duration_lst: list, expected_finish_lst: list) -> dict:
    batch_dict = {batch_lst[i]: (duration_lst[i], expected_finish_lst[i]) for i in range(0, len(batch_lst))}
    return batch_dict


def create_result_batch_dictionary(batch_lst: list, start_datetime_lst: list, delta_time_lst: list) -> dict:
    batch_dict = {batch_lst[i]: (start_datetime_lst[i], delta_time_lst[i]) for i in range(0, len(batch_lst))}
    return batch_dict


def create_dynamic_ordering_constraint(index: int) -> str:
    """
    Creates a valid AMPL constraint of the form:
    [LaTex]: $start\_time_j+1 >= start\_time_j + duration_j$, $\forall j \in BATCH$
    :param index: j index where the current constraint should start
    :return: single AMPL JIT constraint as a string
    """
    i = str(index)
    i_next = str(index + 1)
    constraint_name = f'ordering_{i_next}_{i}'
    return f's.t. {constraint_name}: start_time[{i_next}] >= start_time[{i}] + duration[{i}];'


def create_multiple_ordering_constraints(start_index: int, last_index: int) -> str:
    constraints = ''
    for i in range(start_index, last_index):
        constraints += f'{create_dynamic_ordering_constraint(i)}\n'
    return constraints


def create_multiple_constraints(start_index: int, last_index: int, create_constraints: Callable[[int, int], str]):
    return create_constraints(start_index, last_index)


def dict_to_list(obj: dict) -> list:
    """
    Converts a dictionary to a list, extracting the values of the dictionary.
    The list is sorted according to the dict's keys ascendant order.
    The given dictionary should always have the same numeric keys as the result of create_batch_dictionary().
    :param obj: the dictionary to convert which should have numeric keys
    :return: the list of values in the dictionary
    """
    return list(obj.values())


def strings_to_datetimes(str_date_lst: list, datetime_format: str) -> list:
    """
    Converts a list of strings into a list of datetime objects
    :param str_date_lst: list of string objects compatible with the ISO8601 format
    :param datetime_format: format of the datetime
    :return: list of datetime objects equivalent to the given str_date_lst
    """
    return [datetime.strptime(d, datetime_format) for d in str_date_lst]


def minute_timedelta(first: datetime, second: datetime) -> int:
    """
    Returns the difference expressed in minutes between 2 datetime objects
    :param first: datetime object that comes before second
    :param second: datetime object that comes after first
    :return: difference in minutes between second and first
    """
    delta: timedelta = second - first
    return divmod(delta.total_seconds(), 60)[0]


def minute_timedeltas_wrt_first(datetime_lst: list) -> list:
    """
    Converts a list of datetime objects into a list of minute time deltas with respect to the first item.
    For example, given the input datetime_lst:
    [
        '2019-08-22 14:32',
        '2019-08-22 14:38',
        '2019-08-22 14:42',
        '2019-08-22 14:52',
        '2019-08-22 14:57'
    ],
    the result would be:
    [32, 38, 42, 52, 57]

    :param datetime_lst: list of datetime objects
    :return: minute time deltas with respect to the first item of datetime_lst
    """

    first_datetime: datetime = datetime_lst[0]
    partial_deltas = [minute_timedelta(first=first_datetime, second=v) for v in datetime_lst[1:]]
    first_minutes = first_datetime.minute
    return [first_minutes] + list(map(lambda x: x + first_minutes, partial_deltas))


def set_minutes_to_datetimes(datetime_lst: list, minutes_lst: list) -> list:
    """
    Given a list of minutes and datetime objects, sets each amount of minutes to each datetime object with respect
    to the list index. The two lists must have the same size.
    :param datetime_lst: list of datetime objects
    :param minutes_lst: list of minutes to set to a list of datetime objects
    :return: list of datetime objects similar to datetime_lst but shifted according to minutes_lst
    """
    return [d.replace(minute=0) + timedelta(minutes=m) for d, m in zip(datetime_lst, minutes_lst)]


def datetimes_to_strings(datetime_lst: list, datetime_format: str) -> list:
    """
    Converts a list of datetime objects to strings, according to a certain datetime format.
    :param datetime_lst: list of datetime objects to convert to string
    :param datetime_format: format of the datetime
    :return: the list of datetime objects converted to strings in the given datetime format
    """
    return [d.strftime(datetime_format) for d in datetime_lst]
