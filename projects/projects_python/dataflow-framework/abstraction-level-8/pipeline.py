import importlib
import yaml
from collections import defaultdict, deque
from typing import Dict, List, Iterator, Tuple, Callable, Any
from processor_types import ProcessorFn


def load_processor(path: str) -> ProcessorFn:
    """
    Dynamically import and return a processor function specified by a dotted import path.

    Args:
        path (str): Dotted path to the processor function (e.g. "processors.upper.upper").

    Returns:
        ProcessorFn: The imported processor callable.
    """
    module_path, func_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    func: ProcessorFn = getattr(module, func_name)
    return func


class PipelineNode:
    """
    Represents a node in the DAG pipeline with a processor and downstream routing.
    """

    def __init__(self, name: str, processor: ProcessorFn) -> None:
        """
        Initialize a pipeline node.

        Args:
            name (str): Unique name of the node.
            processor (ProcessorFn): Processor function that processes input lines.
        """
        self.name: str = name
        self.processor: ProcessorFn = processor
        self.downstreams: Dict[str, List["PipelineNode"]] = {}

    def add_downstream(self, tag: str, node: "PipelineNode") -> None:
        """
        Add a downstream node for a specific routing tag.

        Args:
            tag (str): Output tag emitted by this node's processor.
            node (PipelineNode): Downstream node receiving lines tagged with `tag`.
        """
        if tag not in self.downstreams:
            self.downstreams[tag] = []
        self.downstreams[tag].append(node)


class Pipeline:
    """
    Represents the full DAG pipeline, loading configuration, constructing nodes, and executing the DAG.
    """

    def __init__(self, config_path: str) -> None:
        """
        Load and build a DAG pipeline from a YAML configuration.

        Args:
            config_path (str): Path to pipeline YAML config file.
        """
        self.nodes: Dict[str, PipelineNode] = {}
        self.entry_points: List[PipelineNode] = []

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        self._build_from_config(config)

    def _build_from_config(self, config: Dict[str, Any]) -> None:
        """
        Construct pipeline nodes and their routing from a parsed configuration dictionary.

        Args:
            config (Dict[str, Any]): Parsed YAML configuration dictionary.
        """
        nodes_config: Dict[str, Dict[str, Any]] = config["nodes"]

        for node_name, node_info in nodes_config.items():
            proc = load_processor(node_info["type"])
            node = PipelineNode(node_name, proc)
            self.nodes[node_name] = node

        for node_name, node_info in nodes_config.items():
            node = self.nodes[node_name]
            routing: Dict[str, Any] = node_info.get("routes", {})
            for tag, downstream_names in routing.items():
                if isinstance(downstream_names, str):
                    downstream_names = [downstream_names]
                for downstream in downstream_names:
                    node.add_downstream(tag, self.nodes[downstream])

        all_downstream_nodes = set()
        for node in self.nodes.values():
            for downstreams in node.downstreams.values():
                all_downstream_nodes.update(downstreams)

        self.entry_points = [node for node in self.nodes.values() if node not in all_downstream_nodes]

    def run(self, input_lines: Iterator[str]) -> Iterator[str]:
        """
        Run the DAG pipeline on input lines, routing outputs according to tags.

        Args:
            input_lines (Iterator[str]): Iterator of raw input lines to process.

        Yields:
            Iterator[str]: Final processed output lines that have no downstream nodes.
        """
        inputs_map: Dict[str, deque[str]] = defaultdict(deque)
        for entry in self.entry_points:
            inputs_map[entry.name].extend(input_lines)

        output_lines: List[str] = []

        while True:
            progress = False
            for node_name, node in self.nodes.items():
                input_queue = inputs_map[node_name]
                if not input_queue:
                    continue

                def input_gen() -> Iterator[str]:
                    while input_queue:
                        yield input_queue.popleft()

                output_stream: Iterator[Tuple[str, str]] = node.processor(input_gen())

                for tag, line in output_stream:
                    if tag in node.downstreams:
                        for downstream_node in node.downstreams[tag]:
                            inputs_map[downstream_node.name].append(line)
                    else:
                        output_lines.append(line)

                progress = True

            if not progress:
                break

        for line in output_lines:
            yield line
