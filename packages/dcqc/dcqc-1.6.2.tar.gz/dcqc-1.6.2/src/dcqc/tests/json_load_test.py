import json
from pathlib import Path

from dcqc.target import SingleTarget
from dcqc.tests.base_test import InternalBaseTest, TestStatus


class JsonLoadTest(InternalBaseTest):
    tier = 2
    target: SingleTarget

    def compute_status(self) -> TestStatus:
        path = self.target.file.stage()
        if self._can_be_loaded(path):
            status = TestStatus.PASS
        else:
            status = TestStatus.FAIL
        return status

    def _can_be_loaded(self, path: Path) -> bool:
        success = True
        with path.open("r") as infile:
            try:
                json.load(infile)
            except Exception:
                success = False
        return success
