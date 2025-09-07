import yaml
import importlib
from collections import defaultdict, deque
from typing import Any, Callable, Deque, Dict, Iterator, List, Optional, Tuple

from observability.instrumentation import instrument_process


class ProcessorWrapper:
    """
    Wraps a processor function with observability instrumentation.
    """

    def __init__(self, processor_fn: Callable[[Iterator[str]], Iterator[Tuple[str, str]]], processor_name: str) -> None:
        """
        Initialize a wrapped processor.

        Args:
            processor_fn (Callable): The processor function to wrap.
            processor_name (str): Unique name or tag identifying the processor.
        """
        self.fn = processor_fn
        self.name = processor_name

    def process(
        self,
        lines: Iterator[str],
        shared_state: Optional[Any],
        trace_enabled: bool,
        trace_paths: Dict[str, List[str]],
    ) -> Iterator[Tuple[str, str]]:
        """
        Process input lines with instrumentation for metrics, errors, and tracing.

        Args:
            lines (Iterator[str]): Input lines to process.
            shared_state (Optional[Any]): Shared state manager for metrics and errors.
            trace_enabled (bool): Whether tracing is enabled.
            trace_paths (Dict[str, List[str]]): Map of lines to their trace path.

        Yields:
            Iterator[Tuple[str, str]]: Tuples of (next_tag, line).
        """
        yield from instrument_process(self.name, self.fn, lines, shared_state, trace_enabled, trace_paths)


class StateEngine:
    """
    State Machine engine that routes lines between processors based on emitted tags.
    """

    def __init__(self, config_path: str, shared_state: Optional[Any] = None, trace_enabled: bool = False) -> None:
        """
        Initialize the StateEngine from a YAML configuration.

        Args:
            config_path (str): Path to the pipeline state machine configuration file.
            shared_state (Optional[Any]): Shared state manager for metrics and observability.
            trace_enabled (bool): Whether trace recording is enabled.
        """
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.processors: Dict[str, ProcessorWrapper] = {}
        for node in cfg.get("nodes", []):
            tag: str = node["tag"]
            type_path: str = node["type"]
            module_name, fn_name = type_path.rsplit(".", 1)
            mod = importlib.import_module(module_name)
            fn = getattr(mod, fn_name)
            self.processors[tag] = ProcessorWrapper(fn, tag)

        if "start" not in self.processors:
            raise ValueError("Config must define a 'start' processor")
        if "end" not in self.processors:
            raise ValueError("Config must define an 'end' processor")

        self.shared_state = shared_state
        self.trace_enabled = trace_enabled
        self.trace_paths: Dict[str, List[str]] = {}

    def run(self, input_lines: List[str]) -> List[str]:
        """
        Execute the state machine pipeline on the provided input lines.

        Args:
            input_lines (List[str]): Input lines to process.

        Returns:
            List[str]: Final processed outputs emitted by the 'end' processor.
        """
        queue: Deque[Tuple[str, str]] = deque((("start", line) for line in input_lines))
        outputs: List[str] = []
        seen: Dict[Tuple[str, str], int] = defaultdict(int)

        while queue:
            tag, line = queue.popleft()

            if self.trace_enabled:
                if line not in self.trace_paths:
                    self.trace_paths[line] = []
                self.trace_paths[line].append(tag)

            if tag == "end":
                outputs.append(line)
                if self.trace_enabled and self.shared_state:
                    self.shared_state.add_trace(line, self.trace_paths[line])
                continue

            if tag not in self.processors:
                raise ValueError(f"No processor registered for tag '{tag}'")

            seen[(tag, line)] += 1
            if seen[(tag, line)] > 100:
                raise RuntimeError(f"Possible infinite loop detected at tag={tag}, line={line}")

            processor = self.processors[tag]

            for next_tag, next_line in processor.process(
                iter([line]), self.shared_state, self.trace_enabled, self.trace_paths
            ):
                queue.append((next_tag, next_line))

        return outputs
