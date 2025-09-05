import yaml
import importlib
from collections import defaultdict, deque

class ProcessorWrapper:
    """Wraps a processor function or class from processors/."""
    def __init__(self, processor_fn):
        self.fn = processor_fn

    def process(self, lines):
        yield from self.fn(lines)


class StateEngine:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.processors = {}
        for node in cfg.get("nodes", []):
            tag = node["tag"]
            type_path = node["type"]
            module_name, fn_name = type_path.rsplit(".", 1)
            mod = importlib.import_module(module_name)
            fn = getattr(mod, fn_name)
            self.processors[tag] = ProcessorWrapper(fn)

        if "start" not in self.processors:
            raise ValueError("Config must define a 'start' processor")
        if "end" not in self.processors:
            raise ValueError("Config must define an 'end' processor")

    def run(self, input_lines):
        """Run state machine from start until end."""
        queue = deque((("start", line) for line in input_lines))
        outputs = []

        seen = defaultdict(int)  # loop guard

        while queue:
            tag, line = queue.popleft()
            if tag == "end":
                outputs.append(line)
                continue

            if tag not in self.processors:
                raise ValueError(f"No processor registered for tag '{tag}'")

            seen[(tag, line)] += 1
            if seen[(tag, line)] > 100:
                raise RuntimeError(f"Possible infinite loop detected at tag={tag}, line={line}")

            processor = self.processors[tag]
            for next_tag, next_line in processor.process([line]):
                queue.append((next_tag, next_line))

        return outputs
