import json
import threading
from datetime import datetime
from pathlib import Path
from time import sleep

from mlops.common.model import WorkerStatus
from mlops.worker.interfaces import WorkerBase, WorkerStartOptions


class TestingWorker(WorkerBase):
    """
    A testing worker that writes a simple file to the filesystem.
    """

    _status_lock: threading.Lock()
    _close: threading.Event
    _status: WorkerStatus
    _current_task_path: Path = None
    _task_thread: threading.Thread

    def __init__(self):
        self._status = WorkerStatus(
            id='',
            task_type='testing',
            healthy=False,
            has_task=False,
            joined_at=None,
            created_at=datetime.now()
        )
        self._status_lock = threading.Lock()
        self._close = threading.Event()

        self._task_thread = threading.Thread(target=self._loop)
        self._task_thread.start()

    def get_status(self) -> WorkerStatus:
        with self._status_lock:
            return self._status

    def start(self, options: WorkerStartOptions) -> None:
        with self._status_lock:
            self._status.has_task = True
            self._current_task_path = Path(options.task_path)

    def stop(self) -> None:
        with self._status_lock:
            self._status.has_task = False

    def init(self, worker_id: str) -> None:
        with self._status_lock:
            self._status.id = worker_id
            self._status.joined_at = datetime.now()
            self._status.healthy = True

    def shutdown(self) -> None:
        self._close.set()
        self._task_thread.join()

    def _loop(self) -> None:
        while not self._close.wait(0):
            with self._status_lock:
                if not self._status.has_task or self._status.joined_at is None or not self._status.healthy:
                    sleep(10)
                    continue

                task_path = self._current_task_path
            if not (task_path / 'config.json').is_file():
                self._end_task(task_path, False)
                continue

            try:
                cfg = json.load((task_path / 'config.json').open())
            except json.JSONDecodeError:
                self._end_task(task_path, False)
                continue

            if not isinstance(cfg, dict):
                self._end_task(task_path, False)
                continue

            num = cfg.get('num', 5)

            record_file = task_path / 'record.txt'
            with record_file.open('w+') as record:
                cur = record_file.read_text()
                cur = int(cur) if cur != "" else 0
                record.write(str(cur + num))

                if cur >= num:
                    self._end_task(task_path, True)

    def _end_task(self, task_path: Path, success: bool) -> None:
        with task_path / 'status.txt' as status_file:
            status_file.write('success' if success else 'failure')
        self.stop()
