import threading
from collections import defaultdict, deque
from typing import Any, Deque, Dict, List


class SharedState:
    """
    Thread-safe shared state for storing metrics, traces, and errors.

    Metrics:
        - received: Number of items received by each processor.
        - emitted: Number of items emitted by each processor.
        - total_time: Total processing time per processor.
        - errors: Number of errors encountered by each processor.

    Traces:
        Stores recent traces as a deque of dictionaries in the form:
        {"line": line, "path": [list_of_processors]}

    Errors:
        Stores recent errors as a deque of dictionaries in the form:
        {"processor": processor_name, "error": error_message}
    """

    def __init__(self) -> None:
        """Initialize locks and storage for metrics, traces, and errors."""
        self.metrics_lock = threading.Lock()
        self.trace_lock = threading.Lock()
        self.error_lock = threading.Lock()

        self.metrics: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "received": 0,
                "emitted": 0,
                "total_time": 0.0,
                "errors": 0,
            }
        )
        self.traces: Deque[Dict[str, Any]] = deque(maxlen=1000)
        self.errors: Deque[Dict[str, str]] = deque(maxlen=100)

    def increment_received(self, processor_name: str) -> None:
        """Increment the count of received items for a processor."""
        with self.metrics_lock:
            self.metrics[processor_name]["received"] += 1

    def increment_emitted(self, processor_name: str, count: int = 1) -> None:
        """Increment the count of emitted items for a processor."""
        with self.metrics_lock:
            self.metrics[processor_name]["emitted"] += count

    def add_time(self, processor_name: str, duration: float) -> None:
        """Add processing time for a processor."""
        with self.metrics_lock:
            self.metrics[processor_name]["total_time"] += duration

    def increment_error(self, processor_name: str) -> None:
        """Increment the error count for a processor."""
        with self.metrics_lock:
            self.metrics[processor_name]["errors"] += 1

    def add_trace(self, line: Any, path: List[str]) -> None:
        """Add a trace entry for a processed line."""
        with self.trace_lock:
            self.traces.append({"line": line, "path": list(path)})

    def add_error(self, processor_name: str, error_msg: str) -> None:
        """Record an error message for a processor."""
        with self.error_lock:
            self.errors.append({"processor": processor_name, "error": error_msg})

    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve the current metrics snapshot."""
        with self.metrics_lock:
            return dict(self.metrics)

    def get_traces(self) -> List[Dict[str, Any]]:
        """Retrieve the list of recent traces."""
        with self.trace_lock:
            return list(self.traces)

    def get_errors(self) -> List[Dict[str, str]]:
        """Retrieve the list of recent recorded errors."""
        with self.error_lock:
            return list(self.errors)
