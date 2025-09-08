import yaml
import importlib
from collections import defaultdict, deque
from typing import Iterator, List, Tuple
import networkx as nx
import matplotlib.pyplot as plt


class ProcessorWrapper:
    """Wraps a processor function or class from processors directory."""

    def __init__(self, processor_fn):
        self.fn = processor_fn

    def process(self, lines: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
        """Process input tagged lines and yield tagged output lines."""
        yield from self.fn(lines)


class StateEngine:
    def __init__(self, config_path: str, max_visits: int = 1000):
        """
        Load and initialize the state routing engine from config.

        Args:
            config_path: Path to YAML config defining processors and routing.
            max_visits: Max allowed visits per (tag, line) to detect cycles.
        """
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.processors = {}
        self.routing = defaultdict(dict)  # tag -> {output_tag -> list of next tags}
        self.graph = nx.DiGraph()
        self.max_visits = max_visits

        self._load_processors_and_build_graph(cfg)
        self._validate_graph()
        self._validate_tags()

    def _load_processors_and_build_graph(self, cfg: dict):
        """Load processor functions and build routing graph from config."""
        for node in cfg.get("nodes", []):
            tag = node["tag"]
            type_path = node["type"]
            module_name, fn_name = type_path.rsplit(".", 1)
            mod = importlib.import_module(module_name)
            fn = getattr(mod, fn_name)
            self.processors[tag] = ProcessorWrapper(fn)
            self.graph.add_node(tag)

        for node in cfg.get("nodes", []):
            tag = node["tag"]
            routes = node.get("routes", {})
            for out_tag, next_tags in routes.items():
                if isinstance(next_tags, str):
                    next_tags = [next_tags]
                self.routing[tag][out_tag] = next_tags
                for nxt in next_tags:
                    self.graph.add_edge(tag, nxt)

    def _validate_graph(self):
        """Validate graph for required start/end and no cycles."""
        if "start" not in self.processors:
            raise ValueError("Config must define a 'start' processor")
        if "end" not in self.processors:
            raise ValueError("Config must define an 'end' processor")

        if not nx.is_directed_acyclic_graph(self.graph):
            cycles = list(nx.simple_cycles(self.graph))
            cycle_desc = " -> ".join(cycles[0]) if cycles else "unknown"
            raise RuntimeError(f"Config routing graph contains cycles: {cycle_desc}")

    def _validate_tags(self):
        """Ensure all output tags in routing have a registered processor or are 'end'."""
        valid_tags = set(self.processors.keys())
        valid_tags.add("end")
        for from_tag, outputs in self.routing.items():
            for out_tag, next_tags in outputs.items():
                for nxt in next_tags:
                    if nxt not in valid_tags:
                        raise ValueError(f"Routing from '{from_tag}' emits unknown tag '{nxt}'")

    def visualize(self, filename: str = None) -> None:
        pos = nx.spring_layout(self.graph, seed=42)  # fixed seed for consistent layout

        plt.figure(figsize=(8, 6))

        nx.draw_networkx_nodes(self.graph, pos, node_color="lightblue", node_size=2000)
        nx.draw_networkx_labels(self.graph, pos, font_size=12, font_weight="bold")

        nx.draw_networkx_edges(
            self.graph,
            pos,
            arrowstyle="-|>",   # arrow shape
            arrowsize=20,      # size of arrow
            edge_color="gray",
            width=2,
            connectionstyle="arc3,rad=0.1",  # slight curve edges to avoid overlap
            arrows=True
        )

        plt.title("State Routing Graph")
        plt.axis("off")

        if filename:
            plt.savefig(filename)
            print(f"Routing graph saved as {filename}")
            plt.close()
        else:
            plt.show()




    def run(self, input_lines: List[str]) -> List[str]:
        """
        Run the state machine engine from 'start' until lines reach 'end'.

        Args:
            input_lines: List of raw lines to start processing.

        Returns:
            List of output lines tagged as 'end'.
        """
        queue = deque((("start", line) for line in input_lines))
        outputs = []

        seen = defaultdict(int)
        while queue:
            tag, line = queue.popleft()
            if tag == "end":
                outputs.append(line)
                continue

            if tag not in self.processors:
                raise ValueError(f"No processor registered for tag '{tag}'")

            key = (tag, line)
            seen[key] += 1
            if seen[key] > self.max_visits:
                raise RuntimeError(f"Possible infinite loop detected at tag={tag}, line={line}")

            processor = self.processors[tag]
            for next_tag, next_line in processor.process([(tag, line)]):
                next_tags = self.routing.get(tag, {}).get(next_tag)
                if next_tags:
                    for nxt in next_tags:
                        queue.append((nxt, next_line))
                else:
                    queue.append((next_tag, next_line))

        return outputs
