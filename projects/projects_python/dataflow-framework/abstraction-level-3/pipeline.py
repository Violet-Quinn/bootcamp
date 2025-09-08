import yaml
from typing import List
from importlib import import_module
from processor_types import ProcessorFn

def load_function(dotted_path: str) -> ProcessorFn:
    """Dynamically load a function from a dotted import path."""
    module_path, func_name = dotted_path.rsplit('.', 1)
    module = import_module(module_path)
    func = getattr(module, func_name)
    return func

def load_pipeline_from_config(config_path: str) -> List[ProcessorFn]:
    """Parse YAML config, load processor functions dynamically, and return the pipeline list."""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    pipeline_config = config.get("pipeline", [])
    processors: List[ProcessorFn] = []
    for step in pipeline_config:
        func_path = step["type"]
        processor = load_function(func_path)
        processors.append(processor)
    return processors
