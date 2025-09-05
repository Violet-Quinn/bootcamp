import importlib
import yaml
from typing import Dict, List, Iterator, Tuple
from processor_types import ProcessorFn

def load_processor(path: str) -> ProcessorFn:
    """
    Dynamically import and return a processor function specified by a dotted import path.

    Args:
        path: Dotted path to the processor function (e.g. "processors.upper.upper").

    Returns:
        The imported processor callable.
    """
    module_path, func_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    func = getattr(module, func_name)
    return func

class PipelineNode:
    """
    Represents a node in the DAG pipeline with a processor and downstream routing.
    """

    def __init__(self, name: str, processor: ProcessorFn):
        """
        Initialize a pipeline node.

        Args:
            name: Unique name of the node.
            processor: Processor function that processes input lines.
        """
        self.name = name
        self.processor = processor
        self.downstreams = {}

    def add_downstream(self, tag: str, node: "PipelineNode"):
        """
        Add a downstream node for a specific routing tag.

        Args:
            tag: Output tag emitted by this node's processor.
            node: Downstream PipelineNode receiving lines tagged with `tag`.
        """
        if tag not in self.downstreams:
            self.downstreams[tag] = []
        self.downstreams[tag].append(node)

class Pipeline:
    """
    Represents the full DAG pipeline, loading configuration, constructing nodes, and running the pipeline.
    """

    def __init__(self, config_path: str):
        """
        Load and build pipeline from YAML configuration.

        Args:
            config_path: Path to pipeline YAML config file.
        """
        self.nodes: Dict[str, PipelineNode] = {}
        self.entry_points: List[PipelineNode] = []

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        self._build_from_config(config)

    def _build_from_config(self, config):
        """
        Construct pipeline nodes and routing from config dictionary.

        Args:
            config: Parsed YAML config dictionary.
        """
        nodes_config = config["nodes"]
        for node_name, node_info in nodes_config.items():
            proc = load_processor(node_info["type"])
            node = PipelineNode(node_name, proc)
            self.nodes[node_name] = node

        for node_name, node_info in nodes_config.items():
            node = self.nodes[node_name]
            routing = node_info.get("routes", {})
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
            input_lines: Iterator of raw input lines to process.

        Yields:
            Final processed output lines that have no downstream nodes.
        """
        from collections import deque, defaultdict

        inputs_map = defaultdict(deque)
        for entry in self.entry_points:
            inputs_map[entry.name].extend(input_lines)

        output_lines = []

        while True:
            progress = False
            for node_name, node in self.nodes.items():
                input_queue = inputs_map[node_name]
                if not input_queue:
                    continue

                def input_gen():
                    while input_queue:
                        yield input_queue.popleft()

                output_stream = node.processor(input_gen())

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
