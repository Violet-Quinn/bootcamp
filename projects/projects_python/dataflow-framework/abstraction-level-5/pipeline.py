import yaml
from typing import Dict, Callable, Tuple, List, Iterator
from importlib import import_module
from processor_types import ProcessorFn, TaggedLine

def load_function(dotted_path: str) -> Callable:
    module_path, func_name = dotted_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, func_name)

def line_fn_to_dag_processor(fn: Callable[[str], str]) -> ProcessorFn:
    def processor(lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        for tag, line in lines:
            yield tag or "default", fn(line)
    return processor

def load_dag_pipeline(config_path: str) -> Tuple[Dict[str, ProcessorFn], Dict[str, Dict[str, List[str]]]]:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    processors: Dict[str, ProcessorFn] = {}
    for node in config["nodes"]:
        func = load_function(node["processor"])

        # Wrap simple str->str functions
        if callable(func) and hasattr(func, "__code__") and func.__code__.co_argcount == 1:
            func = line_fn_to_dag_processor(func)
        # Instantiate class-based processors
        if isinstance(func, type):
            func = func()

        processors[node["name"]] = func

    routes: Dict[str, Dict[str, List[str]]] = {}
    for route in config.get("routes", []):
        node = route["from"]
        tag = route["tag"]
        to_nodes = route["to"]
        routes.setdefault(node, {}).setdefault(tag, []).extend(to_nodes)

    return processors, routes
