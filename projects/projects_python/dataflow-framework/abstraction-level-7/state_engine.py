import yaml
import importlib
from collections import defaultdict, deque
from typing import Iterator, List, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt
import time
import threading


class ProcessorWrapper:
    def __init__(self, processor_fn):
        self.fn = processor_fn

    def process(self, lines: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
        yield from self.fn(lines)

class StateEngine:
    def __init__(self, config_path: str, max_visits: int = 1000, trace: bool = False):
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.processors = {}
        self.routing = defaultdict(dict)
        self.graph = nx.DiGraph()
        self.max_visits = max_visits
        self.enable_trace = trace

        # Metrics: {processor: {"count": int, "time": float, "errors": int}}
        self.metrics = defaultdict(lambda: {"count": 0, "time": 0.0, "errors": 0})
        self.metrics_lock = threading.Lock()

        # Traces: deque of tuples (line_content, [list of states])
        self.traces = deque(maxlen=1000)
        self.traces_lock = threading.Lock()

        # Errors: deque of tuples (processor_tag, error_message)
        self.errors = deque(maxlen=100)
        self.errors_lock = threading.Lock()

        self._load_processors_and_build_graph(cfg)
        self._validate_graph()
        self._validate_tags()


    def _load_processors_and_build_graph(self, cfg: dict):
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
        if "start" not in self.processors:
            raise ValueError("Config must define a 'start' processor")
        if "end" not in self.processors:
            raise ValueError("Config must define an 'end' processor")

        if not nx.is_directed_acyclic_graph(self.graph):
            cycles = list(nx.simple_cycles(self.graph))
            cycle_desc = " -> ".join(cycles[0]) if cycles else "unknown"
            raise RuntimeError(f"Config routing graph contains cycles: {cycle_desc}")

    def _validate_tags(self):
        valid_tags = set(self.processors.keys())
        valid_tags.add("end")
        for from_tag, outputs in self.routing.items():
            for out_tag, next_tags in outputs.items():
                for nxt in next_tags:
                    if nxt not in valid_tags:
                        raise ValueError(f"Routing from '{from_tag}' emits unknown tag '{nxt}'")

    def visualize(self, filename: Optional[str] = None) -> None:
        pos = nx.spring_layout(self.graph, seed=42)
        plt.figure(figsize=(8, 6))

        nx.draw_networkx_nodes(self.graph, pos, node_color="lightblue", node_size=2000)
        nx.draw_networkx_labels(self.graph, pos, font_size=12, font_weight="bold")
        nx.draw_networkx_edges(
            self.graph,
            pos,
            arrowstyle="-|>", arrowsize=20, edge_color="gray",
            width=2, connectionstyle="arc3,rad=0.1", arrows=True
        )

        plt.title("State Routing Graph")
        plt.axis("off")

        if filename:
            plt.savefig(filename)
            plt.close()
        else:
            plt.show()

    def run(self, input_lines: List[str]) -> List[str]:
        queue = deque((("start", line, ["start"]) for line in input_lines))
        outputs = []

        seen = defaultdict(int)

        while queue:
            tag, line, trace_path = queue.popleft()
            if tag == "end":
                outputs.append(line)
                if self.enable_trace:
                    with self.traces_lock:
                        self.traces.append((line, trace_path))
                continue

            if tag not in self.processors:
                raise ValueError(f"No processor registered for tag '{tag}'")

            key = (tag, line)
            seen[key] += 1
            if seen[key] > self.max_visits:
                raise RuntimeError(f"Possible infinite loop detected at tag={tag}, line={line}")

            processor = self.processors[tag]
            start_time = time.perf_counter()

            try:
                results = list(processor.process([(tag, line)]))
            except Exception as e:
                with self.metrics_lock:
                    self.metrics[tag]["errors"] += 1
                with self.errors_lock:
                    self.errors.append((tag, str(e)))
                continue

            elapsed = time.perf_counter() - start_time
            with self.metrics_lock:
                self.metrics[tag]["count"] += 1
                self.metrics[tag]["time"] += elapsed

            for next_tag, next_line in results:
                next_trace_path = trace_path + [next_tag] if self.enable_trace else []
                next_tags = self.routing.get(tag, {}).get(next_tag)
                if next_tags:
                    for nxt in next_tags:
                        queue.append((nxt, next_line, next_trace_path))
                else:
                    queue.append((next_tag, next_line, next_trace_path))

        return outputs
