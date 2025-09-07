import threading
from collections import defaultdict, deque
from typing import Any, Deque, Dict, List, Optional


class SharedState:
    """
    Thread-safe shared state for storing metrics, traces, errors, and folder queue stats.

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

    Folder Queue Stats:
        - Number of files in unprocessed, underprocess, and processed folders.
        - Currently processing file name.
        - History of last N processed files with timestamps.
    """

    def __init__(self) -> None:
        """Initialize locks and storage for metrics, traces, errors, and folder stats."""
        self.metrics_lock = threading.Lock()
        self.trace_lock = threading.Lock()
        self.error_lock = threading.Lock()
        self.folder_counts_lock = threading.Lock()
        self.current_file_lock = threading.Lock()
        self.processed_files_lock = threading.Lock()

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

        # Folder queue stats initialization
        self.folder_counts: Dict[str, int] = {
            "unprocessed": 0,
            "underprocess": 0,
            "processed": 0,
        }
        self.current_file: Optional[str] = None
        self.processed_files: List[Dict[str, str]] = []

    # --- Metrics methods ---

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

    # --- Trace methods ---

    def add_trace(self, line: Any, path: List[str]) -> None:
        """Add a trace entry for a processed line."""
        with self.trace_lock:
            self.traces.append({"line": line, "path": list(path)})

    def get_traces(self) -> List[Dict[str, Any]]:
        """Retrieve the list of recent traces."""
        with self.trace_lock:
            return list(self.traces)

    # --- Error methods ---

    def add_error(self, processor_name: str, error_msg: str) -> None:
        """Record an error message for a processor."""
        with self.error_lock:
            self.errors.append({"processor": processor_name, "error": error_msg})

    def get_errors(self) -> List[Dict[str, str]]:
        """Retrieve the list of recent recorded errors."""
        with self.error_lock:
            return list(self.errors)

    # --- Metrics retrieval ---

    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve the current metrics snapshot."""
        with self.metrics_lock:
            return dict(self.metrics)

    # --- Folder queue stats methods ---

    def set_folder_counts(self, counts: Dict[str, int]) -> None:
        """Set counts of files in each folder."""
        with self.folder_counts_lock:
            self.folder_counts = dict(counts)

    def get_folder_counts(self) -> Dict[str, int]:
        """Get current counts of files in each folder."""
        with self.folder_counts_lock:
            return dict(self.folder_counts)

    def set_current_file(self, filename: Optional[str]) -> None:
        """Set the name of the currently processing file."""
        with self.current_file_lock:
            self.current_file = filename

    def get_current_file(self) -> Optional[str]:
        """Get the currently processing file name."""
        with self.current_file_lock:
            return self.current_file

    def set_processed_file_history(self, entries: List[Dict[str, str]]) -> None:
        """Set the list of last processed files with timestamps."""
        with self.processed_files_lock:
            self.processed_files = list(entries)

    def get_processed_file_history(self) -> List[Dict[str, str]]:
        """Get the list of last processed files with timestamps."""
        with self.processed_files_lock:
            return list(self.processed_files)
