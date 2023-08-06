import copy
import dataclasses
import logging
import typing
from .cache_manager import CachedOutputs
from .variable import Variable, EnvironmentVariable

logger = logging.getLogger(__name__)


class ExecutionLogger:
    """Log the execution of Tasks.

       Note that this object has longer lifetime than Context.
       One job can have multiple Context objects, but only one ExecutionLogger object.

       Task execution time is not logged in this class since we want to add a log entry before the task execution.
    """
    def __init__(self):
        self._logs = []

    def __deepcopy__(self, memo):
        return self  # Always return the same object

    def log(self, name, task_name, task_version, task_hash, config_dict, inputs_dict, cache_hit):
        record = {'name': name,
                  'task_name': task_name,
                  'task_version': task_version,
                  'task_hash': task_hash,
                  'config': config_dict,
                  'inputs': inputs_dict,
                  'cache_hit': cache_hit}
        self._logs.append(record)

    def get(self):
        return copy.deepcopy(self._logs)


class Context:
    """Manage variables for a single experiment."""
    def __init__(self, environment_variables: typing.Dict[str, str] = None, cache_manager=None):
        self._envs = copy.deepcopy(environment_variables or {})
        self._cache_manager = cache_manager
        self._outputs = {}
        self._execution_logger = ExecutionLogger()

    @property
    def is_cache_enabled(self):
        return bool(self._cache_manager)

    def add_outputs(self, name: str, outputs: typing.Union[dataclasses.dataclass, CachedOutputs]):
        """Add Task outputs to the context so that subsequent Tasks can consume them.

        Args:
            name (str): the name of the task.
            outputs (Outputs or CachedOutputs instance): the outputs of the task.
        """
        if name in self._outputs:
            logger.warning(f"Duplicated task name: {name}. The outputs are overwritten.")
        self._outputs[name] = outputs

    def get_outputs(self, output_name: str):
        """Get the outputs of previous tasks.
        Args:
            name (str): the name of the task
        Returns:
            Outputs dataclass. If the task had been skipped, returns CachedOutputs.
        """
        if output_name not in self._outputs:
            raise ValueError(f"Output {output_name} is not found.")
        return self._outputs[output_name]

    def add_environment_variable(self, name: str, value: str):
        self._envs[name] = value

    def get_environment_variable(self, name: str):
        if name not in self._envs:
            raise ValueError(f"Environment variable {name} is not found.")
        return self._envs[name]

    def resolve(self, value):
        """Recursively replace Variables with actual value.

        Supported containers are:
            - Dict
            - List
            - dataclasses.dataclass
        """
        if isinstance(value, dict):
            return {k: self.resolve(v) for k, v in value.items()}
        elif dataclasses.is_dataclass(value):
            return type(value)(**{field.name: self.resolve(getattr(value, field.name)) for field in dataclasses.fields(value)})
        elif isinstance(value, list):
            return [self.resolve(v) for v in value]
        elif isinstance(value, Variable):
            return value.resolve(self)
        else:
            return value

    def get_cached_outputs(self, task_name, task_version, task_hash: str, outputs_class) -> typing.Optional[CachedOutputs]:
        """Try to get cached outputs for the given task

        Args:
            task_name (str): Task name
            task_version (str): Task version
            task_hash (str): Task hash
            output_class (dataclass): The dataclass of the outputs

        Returns:
            CachedOutput instance if there is a cache. If not, returns None.
        """
        if not self._cache_manager:
            return None

        logger.debug(f"Trying to get cache for Task {task_name} version {task_version}. Hash: {task_hash}")
        return self._cache_manager.get_cache(task_name, task_version, task_hash, outputs_class)

    def add_cache_outputs(self, task_name, task_version, task_hash: str, outputs):
        """Save the task outputs to the cache storage."""
        if self._cache_manager:
            logger.debug(f"Uploading cache for Task {task_name} version {task_version}. Hash: {task_hash}")
            self._cache_manager.upload_cache(task_name, task_version, task_hash, outputs)

    def get_execution_logs(self):
        return self._execution_logger.get()

    def add_execution_log(self, name, task_name, task_version, task_hash, config_dict, inputs_dict, cache_hit):
        self._execution_logger.log(name, task_name, task_version, task_hash, self._resolve_envs(config_dict), self._resolve_envs(inputs_dict), cache_hit)

    def clone(self):
        return copy.deepcopy(self)

    def _resolve_envs(self, value):
        """Recursively replace Variables with actual value. Only replace environment variables.

        """
        if isinstance(value, dict):
            return {k: self._resolve_envs(v) for k, v in value.items()}
        elif dataclasses.is_dataclass(value):
            return {field.name: self._resolve_envs(getattr(value, field.name)) for field in dataclasses.fields(value)}
        elif isinstance(value, list):
            return [self._resolve_envs(v) for v in value]
        elif isinstance(value, EnvironmentVariable):
            try:
                resolved_value = value.resolve(self)
                if isinstance(resolved_value, (int, float, str, bool)):  # Only primitive types are allowed. We need to enforce str-only env variable in the future.
                    return resolved_value
            except ValueError:
                pass
            return str(value)
        elif isinstance(value, Variable):
            return str(value)  # We cannot afford to retrieve cached outputs.
        else:
            return value
