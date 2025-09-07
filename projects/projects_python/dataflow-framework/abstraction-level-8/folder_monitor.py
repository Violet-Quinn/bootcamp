import os
import time
from typing import Optional, List
from threading import Lock

from state_engine import StateEngine
from observability.shared_state import SharedState
from utils import atomic_move, timestamp_now


class FolderMonitor:
    """
    Monitors watch_dir/unprocessed for new files, moves files through states,
    processes them via a state machine pipeline, writes output to processed/,
    and updates shared observability state.
    """

    def __init__(self, watch_dir: str, shared_state: SharedState, trace_enabled: bool = False):
        self.watch_dir = os.path.abspath(watch_dir)
        self.unprocessed_dir = os.path.join(self.watch_dir, "unprocessed")
        self.underprocess_dir = os.path.join(self.watch_dir, "underprocess")
        self.processed_dir = os.path.join(self.watch_dir, "processed")

        for d in (self.unprocessed_dir, self.underprocess_dir, self.processed_dir):
            os.makedirs(d, exist_ok=True)

        self.shared_state = shared_state
        self.trace_enabled = trace_enabled

        self.current_file_lock = Lock()
        self.current_file: Optional[str] = None
        self.processed_files: List[dict] = []

        self.state_engine = StateEngine("pipeline_state.yaml", shared_state, trace_enabled)

        self._recover_incomplete_files()

    def _recover_incomplete_files(self) -> None:
        for filename in os.listdir(self.underprocess_dir):
            try:
                src = os.path.join(self.underprocess_dir, filename)
                dst = os.path.join(self.unprocessed_dir, filename)
                atomic_move(src, dst)
            except Exception as e:
                print(f"[Recovery] Failed to move {src} to {dst}: {e}")

    def _update_folder_metrics(self) -> None:
        counts = {
            "unprocessed": len(os.listdir(self.unprocessed_dir)),
            "underprocess": len(os.listdir(self.underprocess_dir)),
            "processed": len(os.listdir(self.processed_dir)),
        }
        self.shared_state.set_folder_counts(counts)

    def _set_current_file(self, filename: Optional[str]) -> None:
        with self.current_file_lock:
            self.current_file = filename
            self.shared_state.set_current_file(filename)

    def _append_processed_file(self, filename: str) -> None:
        entry = {"filename": filename, "timestamp": timestamp_now()}
        self.processed_files.append(entry)
        if len(self.processed_files) > 100:
            self.processed_files.pop(0)
        self.shared_state.set_processed_file_history(self.processed_files)

    def _process_file(self, filepath: str) -> List[str]:
        self._set_current_file(os.path.basename(filepath))
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                input_lines = [line.strip() for line in f if line.strip()]

            outputs = list(self.state_engine.run(input_lines))
            return outputs
        finally:
            self._set_current_file(None)

    def run_forever(self, poll_interval: float = 1.0) -> None:
        self._update_folder_metrics()
        while True:
            try:
                self._update_folder_metrics()
                files = sorted(os.listdir(self.unprocessed_dir))
                if not files:
                    time.sleep(poll_interval)
                    continue

                for filename in files:
                    src_path = os.path.join(self.unprocessed_dir, filename)
                    underprocess_path = os.path.join(self.underprocess_dir, filename)
                    processed_path = os.path.join(self.processed_dir, filename)

                    try:
                        atomic_move(src_path, underprocess_path)
                        self._update_folder_metrics()

                        outputs = self._process_file(underprocess_path)

                        # Write processed output back to the processed directory file
                        with open(processed_path, "w", encoding="utf-8") as out_f:
                            for line in outputs:
                                out_f.write(line + "\n")

                        # Remove original underprocess file as processed output saved
                        if os.path.exists(underprocess_path):
                            os.remove(underprocess_path)

                        self._append_processed_file(filename)
                        self._update_folder_metrics()

                    except Exception as e:
                        print(f"[Error] Processing file {filename} failed: {e}")

                        # Attempt to move file back to unprocessed for retry
                        try:
                            if os.path.exists(underprocess_path):
                                atomic_move(underprocess_path, src_path)
                        except Exception as inner_e:
                            print(f"[Error] Failed to recover file {filename}: {inner_e}")

                time.sleep(poll_interval)

            except Exception as e:
                print(f"[Error] Folder monitor unexpected error: {e}")
                time.sleep(poll_interval)
