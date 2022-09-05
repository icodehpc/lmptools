from abc import abstractmethod

from ..core.simulation import DumpSnapshot
from ..dump.base import DumpCallback


class SnapshotWriter(DumpCallback):
    """Abstract base class for implementing a snapshot writer"""

    @abstractmethod
    def on_snapshot_parse_end(self, snapshot: DumpSnapshot, *args, **kwargs):
        pass
