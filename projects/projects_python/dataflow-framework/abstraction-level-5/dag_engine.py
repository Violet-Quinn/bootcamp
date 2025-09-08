from typing import Dict, Iterator, List, Tuple
from processor_types import TaggedLine, ProcessorFn

class DAGEngine:
    def __init__(self, processors: Dict[str, ProcessorFn], routes: Dict[str, Dict[str, List[str]]]):
        self.processors = processors
        self.routes = routes

    def run(self, input_lines: Iterator[str], start_node: str) -> Iterator[str]:
        # Start with input lines tagged with default None
        queue: List[Tuple[str, Iterator[TaggedLine]]] = [(start_node, ((None, line) for line in input_lines))]
        completed_outputs: List[str] = []

        while queue:
            node, lines = queue.pop(0)
            processor = self.processors[node]
            out_stream = processor(lines)
            next_inputs: Dict[str, List[Tuple[str, str]]] = {}

            for tag, line in out_stream:
                tag = tag or "default"
                next_nodes = self.routes.get(node, {}).get(tag, [])
                if next_nodes:
                    for nxt_node in next_nodes:
                        next_inputs.setdefault(nxt_node, []).append((tag, line))
                else:
                    # No downstream, collect output here
                    completed_outputs.append(line)

            # Enqueue next inputs
            for nxt_node, tagged_lines in next_inputs.items():
                queue.append((nxt_node, iter(tagged_lines)))

        yield from completed_outputs
