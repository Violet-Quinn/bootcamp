import time
import traceback
from typing import Any, Callable, Dict, Iterable, Iterator, List, Tuple


def instrument_process(
    processor_name: str,
    process_fn: Callable[[Iterable[Any]], Iterable[Tuple[Any, Any]]],
    lines: Iterable[Any],
    shared_state: Any,
    trace_enabled: bool,
    trace_paths: Dict[Any, List[str]],
) -> Iterator[Tuple[Any, Any]]:
    """
    Wrap a processing function with instrumentation for metrics, timing, error handling, and tracing.

    Args:
        processor_name (str): The name of the processor being instrumented.
        process_fn (Callable): The function that processes the input lines.
        lines (Iterable[Any]): Input lines to be processed.
        shared_state (Any): Object that manages metrics, timing, and error tracking.
        trace_enabled (bool): Whether to enable trace recording for processed lines.
        trace_paths (Dict[Any, List[str]]): Mapping of lines to trace paths already visited.

    Yields:
        Iterator[Tuple[Any, Any]]: Tuples of (tag, line) produced by the processor.
    """
    shared_state.increment_received(processor_name)
    start = time.perf_counter()

    try:
        for tag, line in process_fn(lines):
            shared_state.increment_emitted(processor_name)
            if trace_enabled:
                if line not in trace_paths:
                    trace_paths[line] = []
                trace_paths[line].append(processor_name)
            yield tag, line
    except Exception as e:
        shared_state.increment_error(processor_name)
        err_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        shared_state.add_error(processor_name, err_msg)
        return
    finally:
        duration = time.perf_counter() - start
        shared_state.add_time(processor_name, duration)
