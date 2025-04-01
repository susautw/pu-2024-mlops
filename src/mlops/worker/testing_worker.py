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
    _cluster: WorkerClusterWorkerControllerBase | None = None

    __TYPE__ = "testing"
    __VERSION__ = "0.1.0"

    def __init__(self):
        self._status = WorkerStatus(
            id="",
            task_type=self.__TYPE__,
            version=self.__VERSION__,
            healthy=False,
            has_task=False,
            joined_at=None,
            created_at=datetime.now(),
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
        worker_id = cluster.check_in(
            WorkerData(
                host=options.host,
                port=options.port,
                task_type=self.__TYPE__,
                version=self.__VERSION__,
                options={},
            )
        )

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
                if (
                    not self._status.has_task
                    or self._status.joined_at is None
                    or not self._status.healthy
                ):
                    sleep(10)
                    continue

                if self._current_task_path is None:
                    self.stop()
                    continue

                output_path = self._current_task_path / "output"
                assert not output_path.is_file()
                output_path.mkdir(parents=True, exist_ok=True)
            if not (output_path / "config.json").is_file():
                self._end_task(output_path, False)
                continue

            try:
                cfg = json.load((output_path / "config.json").open())
            except json.JSONDecodeError:
                self._end_task(output_path, False)
                continue

            if not isinstance(cfg, dict):
                self._end_task(output_path, False)
                continue

            num = cfg.get("num", 5)

            record_file = output_path / "record.txt"
            with record_file.open("w+") as record:
                cur = record_file.read_text()
                cur = int(cur) if cur != "" else 0
                record.write(str(cur + num))

                if cur >= num:
                    self._end_task(output_path, True)

    def _end_task(self, task_path: Path, success: bool) -> None:
        with (task_path / "status.txt").open("r+") as status_file:
            status_file.write("success" if success else "failure")
        self.stop()

    def __repr__(self):
        return f"<TestingWorker version={self.__VERSION__} status={self.get_status()}>"
