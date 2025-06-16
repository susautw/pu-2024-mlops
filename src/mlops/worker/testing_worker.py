import json
import threading
from datetime import datetime
from pathlib import Path
from time import sleep

from mlops.cluster.interfaces import WorkerClusterWorkerControllerBase
from mlops.common.model import WorkerStatus, WorkerData
from mlops.worker.interfaces import WorkerBase, WorkerStartOptions, WorkerInitOptions


class TestingWorker(WorkerBase):
    """
    A testing worker that writes a simple file to the filesystem.
    """

    _status_lock: threading.RLock
    _close: threading.Event
    _status: WorkerStatus
    _current_task_path: Path | None = None
    _task_thread: threading.Thread
    _cluster: WorkerClusterWorkerControllerBase = None

    __TYPE__ = 'testing'
    __VERSION__ = '0.1.0'

    def __init__(self):
        self._status = WorkerStatus(
            id='',
            task_type=self.__TYPE__,
            version=self.__VERSION__,
            healthy=False,
            has_task=False,
            joined_at=None,
            created_at=datetime.now()
        )
        self._status_lock = threading.RLock()
        self._close = threading.Event()

        self._task_thread = threading.Thread(target=self._loop)
        self._task_thread.start()

    def _report_status(self):
        if self._cluster is not None:
            self._cluster.report_status(self.get_status())

    def get_status(self) -> WorkerStatus:
        with self._status_lock:
            return self._status

    def start(self, options: WorkerStartOptions) -> None:
        with self._status_lock:
            self._status.has_task = True
            self._current_task_path = Path(options.task_path)
            self._report_status()

    def stop(self) -> None:
        with self._status_lock:
            self._status.has_task = False
            self._current_task_path = None
            self._report_status()

    def init(self, cluster: WorkerClusterWorkerControllerBase, options: WorkerInitOptions) -> None:
        self._cluster = cluster
        worker_id = cluster.check_in(WorkerData(
            host=options.host,
            port=options.port,
            task_type=self.__TYPE__,
            version=self.__VERSION__,
            options={}
        ))

        with self._status_lock:
            self._status.id = worker_id
            self._status.joined_at = datetime.now()
            self._status.healthy = True
            _status = self._status

        cluster.report_status(_status)

    def shutdown(self) -> None:
        with self._status_lock:
            # This is a workaround to prevent cluster assigning tasks to this worker
            # currently, the cluster does not have a way to remove a worker from the list
            self._status.healthy = False
            self._report_status()

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
            cur_text = record_file.read_text() if record_file.exists() else ""
            cur = int(cur_text) if cur_text != "" else 0
            new_val = cur + num
            record_file.write_text(str(new_val))

            if new_val >= num:
                self._end_task(task_path, True)

    def _end_task(self, task_path: Path, success: bool) -> None:
        status_file = task_path / 'status.txt'
        with status_file.open('w') as f:
            f.write('success' if success else 'failure')
        self.stop()

    def __repr__(self):
        return f'<TestingWorker version={self.__VERSION__} status={self.get_status()}>'
