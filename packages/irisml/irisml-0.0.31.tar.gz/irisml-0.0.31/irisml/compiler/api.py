import typing

from irisml.compiler.compiler import CompilerSession
from irisml.compiler.stubs import EnvStub, current_session


def get_env(name: str):
    return EnvStub(name)


def make_tasks(func: typing.Callable, **kwargs):
    old_session = current_session.get()
    session = CompilerSession()
    current_session.set(session)
    func(**kwargs)
    current_session.set(old_session)

    job_description = session.generate()
    return [t.to_dict() for t in job_description.tasks]


def on_error(func: typing.Callable):
    old_session = current_session.get()
    session = CompilerSession()
    current_session.set(session)
    func()
    current_session.set(old_session)

    job_description = session.generate()
    if not job_description.tasks:
        raise RuntimeError("on_error must have at least one task")

    old_session.set_on_error(job_description.tasks)
