import yaml
from typing import List
from importlib import import_module
from processor_types import ProcessorFn
from core import line_to_stream_processor

def load_function(dotted_path: str):
    module_path, func_name = dotted_path.rsplit(".", 1)
    module = import_module(module_path)
    func = getattr(module, func_name)
    return func

def load_pipeline_from_config(config_path: str) -> List[ProcessorFn]:
    with open(config_path) as f:
        config = yaml.safe_load(f)
    processors: List[ProcessorFn] = []
    for step in config.get("pipeline", []):
        func_path = step["type"]
        func = load_function(func_path)

        # If it's a class, instantiate it
        if isinstance(func, type):
            func = func()

        # Wrap old style str->str functions with stream adapter
        if callable(func) and not hasattr(func, "__call__") or hasattr(func, "__code__") and getattr(func, "__code__", None) and func.__code__.co_argcount == 1:
            func = line_to_stream_processor(func)

        processors.append(func)
    return processors

