from enum import Enum
from typing import Optional

from ul_api_utils.utils.flask_swagger_generator.exceptions import SwaggerGeneratorError


class InputType(Enum):
    """
    Class SwaggerVersion: Enum for types of swagger version
    """

    INTEGER = 'integer'
    NUMBER = 'number'
    BOOLEAN = 'boolean'
    STRING = 'string'
    ARRAY = 'array'
    OBJECT = 'object'
    NESTED = 'nested'
    DATE_TIME = 'datetime'
    UUID = 'uuid'

    def __repr__(self) -> str:
        return f'{type(self).__name__}.{self.name}'

    @staticmethod
    def from_string(value: str) -> 'InputType':

        if isinstance(value, str):

            if value.lower() in ['integer', 'int']:
                return InputType.INTEGER
            elif value.lower() in ['number', 'num']:
                return InputType.NUMBER
            elif value.lower() in ['boolean', 'bool']:
                return InputType.BOOLEAN
            elif value.lower() in ['string', 'str']:
                return InputType.STRING
            elif value.lower() == 'array':
                return InputType.ARRAY
            elif value.lower() == 'object':
                return InputType.OBJECT
            elif value.lower() == 'nested':
                return InputType.NESTED
            elif value.lower() == 'datetime':
                return InputType.STRING
            elif value.lower() == 'uuid':
                return InputType.UUID
            else:
                raise SwaggerGeneratorError('Could not convert value {} to a input type'.format(value))
        else:
            raise SwaggerGeneratorError("Could not convert non string value to a parameter type")

    def equals(self, other):  # type: ignore

        if isinstance(other, Enum):
            return self.value == other.value
        else:

            try:
                data_base_type = InputType.from_string(other)
                return data_base_type == self
            except SwaggerGeneratorError:
                pass

            return other == self.value

    def get_flask_input_type_value(self) -> Optional[str]:
        if self.value.lower() == 'integer':
            return 'int'
        elif self.value.lower() in 'number':
            return 'num'
        elif self.value.lower() in 'boolean':
            return 'bool'
        elif self.value.lower() in 'string':
            return 'string'
        elif self.value.lower() == 'array':
            return 'array'
        elif self.value.lower() == 'object':
            return 'object'
        elif self.value.lower() == 'uuid':
            return 'uuid'
        return None
