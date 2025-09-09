from collections import deque
from typing import Dict, List, Iterator, Tuple, Callable, Optional
import networkx as nx
import matplotlib.pyplot as plt


def build_routing_graph(
    nodes: Dict[str, Callable[[Iterator[Tuple[str, str]]], Iterator[Tuple[str, str]]]],
    routing_rules: Dict[str, Dict[str, List[str]]],
) -> nx.DiGraph:
    """
    Build a directed graph from nodes and routing rules.

    Args:
        nodes: Dictionary of node_name -> processor callable
        routing_rules: Dict[node_name][tag] -> list of downstream node names

    Returns:
        networkx.DiGraph instance representing the routing graph.
    """
    graph = nx.DiGraph()
    for node in nodes.keys():
        graph.add_node(node)

    for node, tag_routes in routing_rules.items():
        for tag, downstream_nodes in tag_routes.items():
            for down_node in downstream_nodes:
                if down_node not in nodes:
                    raise ValueError(f"Routing rule references unknown node '{down_node}'")
                graph.add_edge(node, down_node)

    if not nx.is_directed_acyclic_graph(graph):
        cycles = list(nx.simple_cycles(graph))
        cycle_str = " -> ".join(cycles[0]) if cycles else "Unknown cycle"
        raise RuntimeError(f"Routing graph contains cycle: {cycle_str}")

    return graph


def visualize_graph(graph: nx.DiGraph, filename: Optional[str] = None) -> None:
    """
    Visualize the routing graph using matplotlib.

    Args:
        graph: networkx.DiGraph instance
        filename: Optional filename to save the plot. If None, shows plot.
    """
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 8))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=2000,
        font_size=12,
        font_weight="bold",
        arrowsize=20,
    )
    plt.title("Routing DAG")
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def route_dag(
    start_node: str,
    nodes: Dict[str, Callable[[Iterator[Tuple[str, str]]], Iterator[Tuple[str, str]]]],
    routing_rules: Dict[str, Dict[str, List[str]]],
    raw_input_lines: Optional[Iterator[str]] = None,
    input_lines: Optional[Iterator[Tuple[str, str]]] = None,
    start_tag: str = "start",
) -> Iterator[str]:
    """
    Route lines through a directed acyclic graph (DAG) of processors based on tags.

    Args:
        start_node: Name of the starting node in the DAG.
        nodes: Mapping of node names to processor callables. Each processor takes an iterator over (tag, line) and yields same.
        routing_rules: Mapping of node names to dicts of tag->list of downstream node names.
        raw_input_lines: Optional iterator of untagged input lines (strings).
        input_lines: Optional iterator of already tagged input lines (tag, line).
        start_tag: Tag to apply to raw input lines if using `raw_input_lines`.

    Yields:
        Processed output lines (strings) from nodes that have no downstream for their tag.
    """
    # Validate input presence
    if input_lines is None:
        if raw_input_lines is None:
            raise ValueError("Must provide either input_lines or raw_input_lines")
        input_lines = ((start_tag, line) for line in raw_input_lines)

    # Validate graph with networkx
    graph = build_routing_graph(nodes, routing_rules)

    # Queues for nodes to hold incoming tagged lines
    queues = {node: deque() for node in nodes}
    queues[start_node].extend(input_lines)

    active_nodes = {start_node}
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
