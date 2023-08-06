import pathlib
import tempfile
import textwrap
import unittest
from irisml.core import JobDescription
from irisml.compiler import Compiler


class TestCompiler(unittest.TestCase):
    def test_simple(self):
        input_str = """
        from irisml.tasks import task_a, task_b

        def main():
            output = task_a()
            output = task_b(in_int=output.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}}]})

        self.check_compile(input_str, expected_job_description)

    def test_unique_names(self):
        input_str = """
        from irisml.tasks import task_a, task_b

        def main():
            output = task_a()
            task_a()
            output2 = task_a()
            task_b(in_int=output.out_int)
            task_b(in_int=output2.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_a'},  # Doesn't have an explicit name because the output is not used.
            {'task': 'task_a', 'name': 'task_a_2'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a_2.out_int'}}]})
        self.check_compile(input_str, expected_job_description)

    def test_manual_names(self):
        input_str = """
        from irisml.tasks import task_a

        def main():
            task_a(_name='my_dataset')
        """
        expected_job_description = JobDescription.from_dict({'tasks': [{'task': 'task_a', 'name': 'my_dataset'}]})
        self.check_compile(input_str, expected_job_description)

    def test_env_variable(self):
        input_str = """
        from irisml.compiler import get_env
        from irisml.tasks import task_a

        def main():
            int_value = get_env('INT_VALUE')
            task_a(in_int=int_value)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [{'task': 'task_a', 'config': {'in_int': '$env.INT_VALUE'}}]})
        self.check_compile(input_str, expected_job_description)

    def test_function_call(self):
        inputs_str = """
        from irisml.tasks import task_a, task_b

        def my_func(int_value):
            return task_b(in_int=int_value)

        def main():
            output = task_a()
            my_func(int_value=output.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}}]})
        self.check_compile(inputs_str, expected_job_description)

    def test_on_error(self):
        input_str = """
        from irisml.tasks import task_a
        from irisml.compiler import on_error

        def main():
            task_a()
            on_error(lambda: task_a())
        """
        expected_job_description = JobDescription.from_dict({'tasks': [{'task': 'task_a'}], 'on_error': [{'task': 'task_a'}]})
        self.check_compile(input_str, expected_job_description)

    def test_child_tasks(self):
        input_str = """
        from irisml.compiler import make_tasks
        from irisml.tasks import task_a, task_c

        def main():
            tasks = make_tasks(lambda: task_a())
            task_c(tasks=tasks)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [{'task': 'task_c', 'config': {'tasks': [{'task': 'task_a'}]}}]})
        self.check_compile(input_str, expected_job_description)

    def test_child_tasks_with_args(self):
        input_str = """
        from irisml.compiler import make_tasks
        from irisml.tasks import task_a, task_b, task_c

        def child_tasks(int_value):
            task_b(in_int=int_value)

        def main():
            output = task_a()
            tasks = make_tasks(child_tasks, int_value=output.out_int)
            task_c(tasks=tasks)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_c', 'config': {'tasks': [{'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}}]}}]})
        self.check_compile(input_str, expected_job_description)

    def check_compile(self, input_str, expected_job_description, build_args={}):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            self._make_fake_tasks(temp_dir)
            input_filepath = temp_dir / 'input.py'
            input_filepath.write_text(textwrap.dedent(input_str))
            compiler = Compiler()
            job_description = compiler.compile(input_filepath, include_paths=[], build_args=build_args)
            print(job_description)
            self.assertEqual(job_description, expected_job_description)

    def test_build_args(self):
        input_str = """
        from irisml.tasks import task_a, task_b

        def main(param, param2, param3):
            if param == '1' and param2 == "single quotes 'hi'" and param3 == 'double quotes ""':
                output = task_a()
                output = task_b(in_int=output.out_int)
        """
        expected_job_description = JobDescription.from_dict({'tasks': [
            {'task': 'task_a'},
            {'task': 'task_b', 'inputs': {'in_int': '$output.task_a.out_int'}}]})

        self.check_compile(input_str, expected_job_description, {'param': '1', 'param2': "single quotes 'hi'", 'param3': 'double quotes ""'})

    def _make_fake_tasks(self, dir_path):
        tasks_dir = dir_path / 'irisml' / 'tasks'
        tasks_dir.mkdir(parents=True)

        (tasks_dir / 'task_a.py').write_text(textwrap.dedent("""
        import dataclasses
        import irisml.core

        class Task(irisml.core.TaskBase):
            @dataclasses.dataclass
            class Config:
                in_int: int = 100

            @dataclasses.dataclass
            class Outputs:
                out_int: int = 42
        """))

        (tasks_dir / 'task_b.py').write_text(textwrap.dedent("""
        import dataclasses
        import irisml.core

        class Task(irisml.core.TaskBase):
            @dataclasses.dataclass
            class Inputs:
                in_int: int
        """))

        (tasks_dir / 'task_c.py').write_text(textwrap.dedent("""
        import dataclasses
        import typing
        from irisml.core import TaskDescription
        import irisml.core

        class Task(irisml.core.TaskBase):
            @dataclasses.dataclass
            class Config:
                tasks: typing.List[TaskDescription]
        """))
