import contextvars
import dataclasses
import importlib
import importlib.util
import sys
import types


current_session = contextvars.ContextVar('current_session')


class TasksModuleStub(types.ModuleType):
    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError()

        stub_tasks = sys.modules['irisml.tasks']
        del sys.modules['irisml.tasks']
        original_module = importlib.import_module(f'irisml.tasks.{name}')
        sys.modules['irisml.tasks'] = stub_tasks
        return TaskStub(name, original_module.Task)


class TaskStub:
    def __init__(self, task_name, original_task):
        self._task_name = task_name
        self._task = original_task

    def __call__(self, **kwargs):
        session = current_session.get()
        name = kwargs.pop('_name', None)

        input_names = [f.name for f in dataclasses.fields(self._task.Inputs)]
        config_names = [f.name for f in dataclasses.fields(self._task.Config)]
        if invalid_names := set(kwargs.keys()) - set(input_names) - set(config_names):
            raise ValueError(f'Invalid arguments: {invalid_names}')

        inputs = {k: kwargs[k] for k in input_names if k in kwargs}
        config = {k: kwargs[k] for k in config_names if k in kwargs}
        assert len(inputs) + len(config) == len(kwargs)
        task_instance = TaskInstance()
        name = session.add_task(task_instance, self._task_name, name, inputs, config)
        return OutputsStub(task_instance, name, self._task.Outputs)

    def __str__(self):
        return f'TaskStub(task={self._task_name})'


class TaskInstance:
    def __init__(self):
        self._reference_counter = 0

    def increment_reference_counter(self):
        self._reference_counter += 1

    @property
    def ref_count(self):
        return self._reference_counter

    def __str__(self):
        return f'TaskInstance(ref_count={self._reference_counter})'


class OutputsStub:
    def __init__(self, task, name, outputs_dataclass):
        self._task = task
        self._name = name
        self._output_types = {f.name: f.type for f in dataclasses.fields(outputs_dataclass)}

    def increment_reference_counter(self):
        self._task.increment_reference_counter()

    def __getattr__(self, name):
        if name not in self._output_types:
            raise AttributeError(f'No output named {name}')
        return OutputsMemberStub(self, self._name, name, self._output_types[name])

    def __str__(self):
        return f'OutputsStub(name={self._name}, outputs={self._output_types})'


class VariableStub:
    def resolve(self):
        return str(self)


class OutputsMemberStub(VariableStub):
    def __init__(self, parent, parent_name, name, data_type):
        self._parent = parent
        self._parent_name = parent_name
        self._name = name
        self._data_type = data_type

    def resolve(self):
        self._parent.increment_reference_counter()
        return super().resolve()

    def __str__(self):
        return f'$output.{self._parent_name}.{self._name}'


class EnvStub(VariableStub):
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return f'$env.{self._name}'
