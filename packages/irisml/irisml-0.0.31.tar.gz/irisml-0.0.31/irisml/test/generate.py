import dataclasses
import importlib
import json
import pathlib
import re
import typing
import unittest
from irisml.core import TaskBase


VALID_NAME_PATTERN = re.compile('[a-z][a-z0-9_]*')


def _generate_test_task_method(filepath):
    def test_method(self):
        print(f"Testing {filepath}")
        task_name = filepath.stem
        self.assertTrue(VALID_NAME_PATTERN.match(task_name))
        task_module = importlib.import_module(f'irisml.tasks.{task_name}')
        task_class = task_module.Task

        self.assertIsNotNone(task_class)
        self.assertTrue(task_class.__doc__, "The Task class must have docstring.")
        self.assertTrue(issubclass(task_class, TaskBase))
        self.assertTrue(task_class.VERSION and task_class.VERSION != '0.0.0')
        self.assertTrue(dataclasses.is_dataclass(task_class.Config))
        self.assertTrue(dataclasses.is_dataclass(task_class.Inputs))
        self.assertTrue(dataclasses.is_dataclass(task_class.Outputs))

        config_names = [f.name for f in dataclasses.fields(task_class.Config)]
        inputs_names = [f.name for f in dataclasses.fields(task_class.Inputs)]
        outputs_names = [f.name for f in dataclasses.fields(task_class.Outputs)]

        self.assertFalse(set(config_names) & set(inputs_names))
        self.assertTrue(all(VALID_NAME_PATTERN.match(n) for n in config_names))
        self.assertTrue(all(VALID_NAME_PATTERN.match(n) for n in inputs_names))
        self.assertTrue(all(VALID_NAME_PATTERN.match(n) for n in outputs_names))
        self.assertTrue(True)

        if task_class.dry_run != TaskBase.dry_run:
            self.assertTrue(all(f.default or f.default_factory for f in dataclasses.fields(task_class.Outputs)), "If dry_run() is not defined, all Outputs fields must have default values.")

    return test_method


def _generate_test_config_method(filepath):
    def test_method(self):
        print(f"Testing {filepath}")
        original_text = filepath.read_text()
        config = json.loads(original_text)

        self.assertIsInstance(config, dict)
        self.assertIn('tasks', config)
        self.assertIsInstance(config['tasks'], list)

        self.assertFalse(set(config.keys()) - {'tasks', 'on_error'})

        # Check the format
        formatted_text = json.dumps(config, sort_keys=False, indent=4) + '\n'
        if original_text != formatted_text:
            self.fail(f"{filepath} is not formatted. Please use 'python -m json.tool' to format the file.")

    return test_method


def generate_task_tests(target_filepaths: typing.List[pathlib.Path]):
    class TestTasks(unittest.TestCase):
        pass

    for filepath in target_filepaths:
        if filepath.stem == '__pycache__':
            continue
        test_name = f'test_{filepath.stem}'
        setattr(TestTasks, test_name, _generate_test_task_method(filepath))

    return TestTasks


def generate_config_tests(target_filepaths: typing.List[pathlib.Path]):
    class TestConfigs(unittest.TestCase):
        pass

    used = set()
    for filepath in target_filepaths:
        test_name = f'test_{filepath.stem}'
        index = 2
        while test_name in used:
            test_name = f'test_{filepath.stem}_{index}'
            index += 1
        used.add(test_name)
        setattr(TestConfigs, test_name, _generate_test_config_method(filepath))

    return TestConfigs
