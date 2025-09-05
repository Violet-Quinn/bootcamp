from processor_types import ProcessorFnTag
from collections import deque
from typing import Dict, List, Iterator, Tuple, Callable, Optional

def route_dag(
    start_node: str,
    nodes: Dict[str, Callable[[Iterator[Tuple[str, str]]], Iterator[Tuple[str, str]]]],
    routing_rules: Dict[str, Dict[str, List[str]]],
    raw_input_lines: Optional[Iterator[str]] = None,
    input_lines: Optional[Iterator[Tuple[str, str]]] = None,
    start_tag: str = "start"
) -> Iterator[str]:
    """
    Route lines through a directed acyclic graph (DAG) of processors based on tags.

    Exactly one of `input_lines` or `raw_input_lines` must be provided. If 
    `raw_input_lines` is given, lines are automatically tagged with `start_tag` 
    and fed to the `start_node`. The function repeatedly processes lines through nodes, 
    forwarding tagged output lines according to routing rules until no more processing 
    can occur. Lines without downstream routes are yielded as final output lines.

    Args:
        start_node: Name of the starting node in the DAG.
        nodes: Mapping of node names to processor callables. Each processor 
               takes an iterator over (tag, line) tuples and yields the same.
        routing_rules: Mapping of node names to dicts of tag->list of downstream node names.
        raw_input_lines: Optional iterator of untagged input lines (strings).
        input_lines: Optional iterator of already tagged input lines (tag, line).
        start_tag: Tag to apply to raw input lines if using `raw_input_lines`.

    Yields:
        Processed output lines (strings) from nodes that have no downstream for their tag.
    """
    if input_lines is None:
        if raw_input_lines is None:
            raise ValueError("Must provide either input_lines or raw_input_lines")
        input_lines = ((start_tag, line) for line in raw_input_lines)

    queues = {node: deque() for node in nodes}
    queues[start_node].extend(input_lines)

    active_nodes = set([start_node])
    output_buffer = deque()

    while active_nodes:
        new_active = set()
        for node in active_nodes:
            proc = nodes[node]
            queue = queues[node]
            if not queue:
                continue

            inputs = []
            while queue:
                tag, line = queue.popleft()
                inputs.append((tag, line))

            outputs = proc(iter(inputs))

            for tag, line in outputs:
                down_nodes = routing_rules.get(node, {}).get(tag, [])
                if down_nodes:
                    for down_node in down_nodes:
                        queues[down_node].append((tag, line))
                        new_active.add(down_node)
                else:
                    output_buffer.append(line)

        while output_buffer:
            yield output_buffer.popleft()

        active_nodes = new_active
