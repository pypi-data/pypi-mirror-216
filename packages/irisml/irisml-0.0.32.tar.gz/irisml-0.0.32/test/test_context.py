import copy
import dataclasses
import typing
import unittest
from irisml.core.context import Context, ExecutionLogger
from irisml.core.variable import EnvironmentVariable, OutputVariable


class TestContext(unittest.TestCase):
    def test_clone(self):
        context = Context({'env': 'value'})
        new_context = context.clone()
        self.assertEqual(new_context.get_environment_variable('env'), 'value')

        new_context.add_environment_variable('env2', 'value2')
        new_context.add_outputs('out', None)

        with self.assertRaises(ValueError):
            context.get_environment_variable('env2')

        with self.assertRaises(ValueError):
            context.get_outputs('out')

    def test_resolve(self):
        context = Context()
        self.assertEqual(context.resolve(123), 123)
        self.assertEqual(context.resolve('123'), '123')
        self.assertEqual(context.resolve([1, 2, 3]), [1, 2, 3])
        self.assertEqual(context.resolve([1, '2', 3]), [1, '2', 3])

        with self.assertRaises(ValueError):
            context.resolve(EnvironmentVariable('$env.E'))

        context = Context({'E': 'v'})
        self.assertEqual(context.resolve(EnvironmentVariable('$env.E')), 'v')
        self.assertEqual(context.resolve([3, EnvironmentVariable('$env.E')]), [3, 'v'])

        class DummyOutput:
            value = 3

        context.add_outputs('test_out', DummyOutput())
        self.assertEqual(context.resolve([123, OutputVariable('$output.test_out.value')]), [123, 3])

    def test_resolve_nested_dataclass(self):
        @dataclasses.dataclass
        class ChildConfig:
            value: int

        @dataclasses.dataclass
        class Config:
            child: ChildConfig

        config = Config(ChildConfig(42))
        context = Context()
        self.assertEqual(context.resolve(config), config)

    def test_add_execution_log(self):
        context = Context({'ENV': 'value'})
        context.add_execution_log('name', 'task_name', '0.0.0', None, {'config': EnvironmentVariable('$env.ENV')}, {}, False)

        logs = context.get_execution_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0], {'name': 'name', 'task_name': 'task_name', 'task_version': '0.0.0', 'task_hash': None, 'config': {'config': 'value'}, 'inputs': {}, 'cache_hit': False})

        @dataclasses.dataclass
        class Outputs:
            value: typing.List[int]

        context.add_outputs('out', Outputs([1, 2, 3]))
        context.add_execution_log('name', 'task_name', '0.0.0', None, {}, {'in': OutputVariable('$output.out.value')}, False)

        logs = context.get_execution_logs()
        self.assertEqual(len(logs), 2)
        # Since the $output.out.value is a list, the value is not resolved
        self.assertEqual(logs[1], {'name': 'name', 'task_name': 'task_name', 'task_version': '0.0.0', 'task_hash': None, 'config': {}, 'inputs': {'in': '$output.out.value'}, 'cache_hit': False})


class TestExecutionLogger(unittest.TestCase):
    def test_deepcopy(self):
        execution_logger = ExecutionLogger()
        execution_logger.log('name', 'task_name', '0.0.0', None, {'config': 0}, {}, False)

        copied_logger = copy.deepcopy(execution_logger)
        copied_logger.log('name', 'task_name', '0.0.0', None, {'config': 1}, {}, False)

        execution_logger.log('name', 'task_name', '0.0.0', None, {'config': 2}, {}, False)

        logs = execution_logger.get()
        self.assertEqual(len(logs), 3)
        self.assertEqual(logs[0], {'name': 'name', 'task_name': 'task_name', 'task_version': '0.0.0', 'task_hash': None, 'config': {'config': 0}, 'inputs': {}, 'cache_hit': False})
        self.assertEqual(logs[1], {'name': 'name', 'task_name': 'task_name', 'task_version': '0.0.0', 'task_hash': None, 'config': {'config': 1}, 'inputs': {}, 'cache_hit': False})
        self.assertEqual(logs[2], {'name': 'name', 'task_name': 'task_name', 'task_version': '0.0.0', 'task_hash': None, 'config': {'config': 2}, 'inputs': {}, 'cache_hit': False})

        copied_logs = copied_logger.get()
        self.assertEqual(logs, copied_logs)
