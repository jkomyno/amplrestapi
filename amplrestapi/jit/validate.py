import logging
from typing import Tuple
from jsonschema import validate as validate_json, ValidationError
from typing import Union

from .utils import is_asc_sorted


def validate(json: dict, schema: str) -> Tuple[bool, Union[str, None]]:
    """
    Validates the given json string against the given JSON schema as well as the logic constraints
    in the input data.
    :param json: JSON string whose structure must be validated
    :param schema: JSON schema that defines what must be validated
    :return: A tuple composed of 2 elements (bool, str | None).
             The first element is True if and only if the validation had success.
             The second element is a string that contains the validation error
             message, if any was thrown.
    """
    try:
        # validate the given JSON against the validation JSON schema
        validate_json(instance=json, schema=schema)

        # the length of `duration` and `expected_finish` must be equal to the value of `n_batches`
        if len(json['duration']) != len(json['expected_finish']) or len(json['duration']) != json['n_batches']:
            return False, 'The length of the `duration` and `expected_finish` lists must equal the value of `n_batches`'

        if not is_asc_sorted(json['expected_finish']):
            return False, 'The values in the `expected_finish` list must be ascendentally sorted'

        return True, None
    except ValidationError as err:
        logging.log(logging.ERROR, err)
        return False, err
