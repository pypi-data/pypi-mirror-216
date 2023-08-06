import logging
import typing
from .cache_manager import CachedOutputs, HashGenerator

logger = logging.getLogger(__name__)


def replace_variables(value):
    """Replace a string '$env' and '$outputs' in the given object with Variable instances."""
    if isinstance(value, dict):
        return {k: replace_variables(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_variables(v) for v in value]
    elif isinstance(value, str) and value and value[0] == '$':
        if value.startswith('$env.'):
            return EnvironmentVariable(value)
        elif value.startswith('$output.'):
            return OutputVariable(value)
        else:
            raise ValueError(f"Unknown variable type: {value}")
    else:
        return value


class Variable:
    """Base class for Variables.

    In a task description, a string with '$' prefix is considered a variable.
    Currently we have two variable types: $env and $output. $env is Environment Variables that can be set to Context. $output is output objests from previous tasks.

    """

    def __init__(self, name):
        self._var_str = name
        self._expected_type = str

    @property
    def expected_type(self):
        return self._expected_type

    @expected_type.setter
    def expected_type(self, value):
        self._expected_type = value

    def __eq__(self, other):
        return type(self) is type(other) and self._var_str == other._var_str

    def __hash__(self):
        return hash(self._var_str)

    def resolve(self, context):
        """Returns the actual value this variable represents."""
        raise NotImplementedError

    def get_hash(self, context):
        """Get hash value for the value that is stored in this Variable."""
        return HashGenerator.calculate_hash(self.resolve(context))


class EnvironmentVariable(Variable):
    """A variable with $env prefix"""

    def __init__(self, name):
        super().__init__(name)
        parts = name.split('.')
        if len(parts) != 2 or parts[0] != '$env' or not parts[1].isupper():
            raise ValueError(f"Invalid environment variable name: {name}")

        self._name = parts[1]

    def resolve(self, context):
        str_value = context.get_environment_variable(self._name)
        typing_origin = typing.get_origin(self._expected_type)
        if typing_origin is typing.Literal:
            value = next((a for a in typing.get_args(self._expected_type) if str(a) == str_value), None)
            if value is None:
                raise ValueError(f"The given string '{str_value}' is not included in the Literal[{typing.get_args(self._expected_type)}]")
            return value
        elif typing_origin is typing.Union:
            if not isinstance(str_value, typing.get_args(self._expected_type)):
                logger.warning(f"{str_value} is expected to have {self._expected_type}, but it is {type(str_value)}")
            # return whatever is stored as it is Union type.
            # Todo: need more strict type check
            return str_value

        if isinstance(str_value, str):
            return self._expected_type(str_value)
        elif not isinstance(str_value, self._expected_type):
            # Todo: need more strict type check
            logger.warning(f"{str_value} is expected to have {self._expected_type}, but it is {type(str_value)}")
        return str_value

    def __str__(self):
        return f"$env.{self._name}"


class OutputVariable(Variable):
    """A variable with $output prefix. Outputs from a task."""

    def __init__(self, name):
        super().__init__(name)
        parts = name.split('.')
        if len(parts) != 3 or parts[0] != '$output' or not name.islower():
            raise ValueError(f"Invalid output variable name: {name}")

        self._name = parts[1]
        self._path = parts[2]

    def resolve(self, context):
        outputs = context.get_outputs(self._name)
        if not hasattr(outputs, self._path):
            raise ValueError(f"Output {self._name} doesn't have path {self._path}")
        return getattr(outputs, self._path)

    def get_hash(self, context):
        outputs = context.get_outputs(self._name)
        if isinstance(outputs, CachedOutputs):
            return outputs.get_hash(self._path)

        if not hasattr(outputs, self._path):
            raise ValueError(f"Output {self._name} doesn't have path {self._path}")
        value = getattr(outputs, self._path)
        return HashGenerator.calculate_hash(value, context)

    def __str__(self):
        return f"$output.{self._name}.{self._path}"
