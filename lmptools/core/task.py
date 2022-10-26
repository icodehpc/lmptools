from __future__ import annotations
from abc import ABC, abstractmethod
from ..dump import DumpSnapshot
from typing import Optional, List


class Task(ABC):
    """ Base Task class """

    @abstractmethod
    def run(self, snapshot: DumpSnapshot, *args, **kwargs) -> Optional[DumpSnapshot]:
        """ Run method to implement the task """
        raise NotImplementedError


class Pipeline:
    def __init__(self, tasks: List[Task]):
        self._tasks = tasks

    def run(self, snapshot: DumpSnapshot, *args, **kwargs):
        for idx, task in enumerate(self.tasks):
            snapshot = task.run(snapshot)
