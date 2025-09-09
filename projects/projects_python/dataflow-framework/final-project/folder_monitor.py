import os
import shutil
import threading
import time
from typing import Optional
from state_engine import StateEngine

class FolderMonitor:
    def __init__(self, watch_dir: str, state_engine: StateEngine, poll_interval: float = 1.0):
        self.watch_dir = watch_dir
        self.unprocessed_dir = os.path.join(watch_dir, "unprocessed")
        self.underprocess_dir = os.path.join(watch_dir, "underprocess")
        self.processed_dir = os.path.join(watch_dir, "processed")
        self.state_engine = state_engine
        self.poll_interval = poll_interval
        self.current_file: Optional[str] = None
        self.current_file_lock = threading.Lock()
        self._setup_dirs()
        self._recover_inprogress_files()

    def _setup_dirs(self):
        os.makedirs(self.unprocessed_dir, exist_ok=True)
        os.makedirs(self.underprocess_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    def _recover_inprogress_files(self):
        files = os.listdir(self.underprocess_dir)
        for f in files:
            src = os.path.join(self.underprocess_dir, f)
            dst = os.path.join(self.unprocessed_dir, f)
            try:
                shutil.move(src, dst)
            except Exception:
                pass  # Ignore errors here

    def _update_metrics(self):
        with self.state_engine.metrics_lock:
            self.state_engine.metrics["folder_monitor"] = {
                "unprocessed": len(os.listdir(self.unprocessed_dir)),
                "underprocess": len(os.listdir(self.underprocess_dir)),
                "processed": len(os.listdir(self.processed_dir)),
            }
        with self.current_file_lock:
            self.state_engine.current_processing_file = self.current_file

    def _process_file(self, filepath: str):
        # Read file, process via state engine, overwrite the file with transformed output
        with open(filepath, "r") as f:
            input_lines = [line.strip() for line in f if line.strip()]
        output_lines = self.state_engine.run(input_lines)
        with open(filepath, "w") as f:
            for line in output_lines:
                f.write(line + "\n")

    def run(self):
        while True:
            try:
                self._update_metrics()
                files = sorted(os.listdir(self.unprocessed_dir))
                if not files:
                    time.sleep(self.poll_interval)
                    continue
                for filename in files:
                    src_path = os.path.join(self.unprocessed_dir, filename)
                    processing_path = os.path.join(self.underprocess_dir, filename)
                    shutil.move(src_path, processing_path)
                    with self.current_file_lock:
                        self.current_file = filename
                    self._update_metrics()
                    try:
                        self._process_file(processing_path)
                    except Exception as e:
                        with self.state_engine.errors_lock:
                            self.state_engine.errors.append(("folder_monitor", f"Error processing {filename}: {e}"))
                    finally:
                        # Move transformed file to processed folder
                        final_path = os.path.join(self.processed_dir, filename)
                        shutil.move(processing_path, final_path)
                        with self.current_file_lock:
                            self.current_file = None
                    self._update_metrics()
            except Exception as e:
                with self.state_engine.errors_lock:
                    self.state_engine.errors.append(("folder_monitor", f"General monitor error: {e}"))
                time.sleep(self.poll_interval)
