from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from ..dump import DumpSnapshot


class Task(ABC):
    """Base Task class"""

    @abstractmethod
    def run(self, snapshot: DumpSnapshot, *args, **kwargs) -> Optional[DumpSnapshot]:
        """Run method to implement the task"""
        raise NotImplementedError


class Pipeline:
    def __init__(self, tasks: List[Task] = []):
        self._tasks = tasks

    def run(self, snapshot: Optional[DumpSnapshot], *args, **kwargs):
        for idx, task in enumerate(self._tasks):
            snapshot = task.run(snapshot)

    def append(self, task: Task):
        """Add tasks to the pipeline"""
        self._tasks.append(task)
