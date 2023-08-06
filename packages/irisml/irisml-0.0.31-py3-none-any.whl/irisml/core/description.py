import dataclasses
from typing import Any, Dict, List, Optional
import typing


def to_dict(x):
    if hasattr(x, 'to_dict'):
        return x.to_dict()
    if isinstance(x, dict):
        return {k: to_dict(v) for k, v in x.items()}
    if isinstance(x, list):
        return [to_dict(v) for v in x]
    return x


@dataclasses.dataclass
class TaskDescription:
    task: str
    name: Optional[str] = None  # Optional name for the task. Must be unique in the job. This name will be used for OutputVariable names.
    inputs: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: typing.Dict):
        return cls(**data)

    def to_dict(self) -> typing.Dict:
        d = {'task': self.task}
        if self.name:
            d['name'] = self.name
        if self.inputs:
            d['inputs'] = to_dict(self.inputs)
        if self.config:
            d['config'] = to_dict(self.config)
        return d


@dataclasses.dataclass
class JobDescription:
    tasks: List[TaskDescription]
    on_error: Optional[List[TaskDescription]]

    @classmethod
    def from_dict(cls, data: typing.Dict):
        c = {'tasks': [TaskDescription.from_dict(t) for t in data['tasks']],
             'on_error': data.get('on_error', None) and [TaskDescription.from_dict(t) for t in data['on_error']]}
        return cls(**c)

    def to_dict(self) -> typing.Dict:
        d = {'tasks': [t.to_dict() for t in self.tasks]}
        if self.on_error:
            d['on_error'] = [t.to_dict() for t in self.on_error]
        return d
